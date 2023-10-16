from django.test import TestCase,RequestFactory
from django.contrib.admin.sites import AdminSite
from apps.users.models import User
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError
from django.conf import settings
from apps.session.models import UserSession, LogRequests
from apps.session.admin import UserSessionAdmin, LogRequestsAdmin
from apps.session.functions import remover_sessao
from django.contrib.auth.password_validation import validate_password

username = 'teste.user'
name = "Teste User"
class SessionModelTest(TestCase):
    def setUp(self):
        user = User(name=name, username=username,password=settings.USER_PASSWORD_TEST,is_staff=True)
        user.save()

        self.client.login(username=username,password=settings.USER_PASSWORD_TEST)
        session_django = Session.objects.filter(session_key=self.client.session.session_key).first()

        session = UserSession(
            user=user,
            session=session_django,
            modificado_em=timezone.now())
        session.save()

        self.user = user
        self.session = session

    def test_online(self):
        self.client.login(username=username,password=settings.USER_PASSWORD_TEST)

        session = UserSession.objects.filter(user=self.user).first()
        self.assertTrue(session.time_online())

class SessionAdminTest(TestCase):
    def setUp(self):
        user = User(name=name, username=username,password=settings.USER_PASSWORD_TEST,is_staff=True)
        user.save()

        self.client.login(username=username,password=settings.USER_PASSWORD_TEST)
        
        session_django = Session.objects.filter(session_key=self.client.session.session_key).first()

        session = UserSession(
            user=user,
            session=session_django,
            modificado_em=timezone.now(),
            criado_em=timezone.now()
        )
        
        session.save()
        admin_site = AdminSite()

        self.user = user
        self.admin_site = admin_site
        self.session = session

        
    def test_action_deslogar(self):
        action_params = {
            'POST': {
                'action': 'remover_sessao',  
                '_selected_action': [str(self.user.pk)],
            }
        }

        remover_sessao(self.admin_site, action_params,UserSession.objects.all())
        session = UserSession.objects.filter(user=self.user).first()
        self.assertFalse(session)

    def test_get_titulo(self):
        user_session_admin = UserSessionAdmin(UserSession,self.admin_site)
        resultado = user_session_admin.get_titulo(self.session)

        self.assertEqual('Sem papel atribuído',resultado)

    def test_get_dt_login(self):
        user_session_admin = UserSessionAdmin(UserSession,self.admin_site)
        resultado = user_session_admin.get_dt_login(self.session)

        self.assertEqual(self.session.criado_em,resultado)

    def test_get_actions(self):
        user_session_admin = UserSessionAdmin(UserSession,self.admin_site)
        
        factory = RequestFactory()
        request = factory.get('/admin/session/usersession/')

        resultado = user_session_admin.get_actions(request=request)

        self.assertTrue(type(resultado) is dict)

    def test_has_add_permission(self): 
        user_session_admin = UserSessionAdmin(UserSession,self.admin_site)
        resultado = user_session_admin.has_add_permission(None,None)

        self.assertFalse(resultado)
    def test_has_change_permission(self): 
        user_session_admin = UserSessionAdmin(UserSession,self.admin_site)
        resultado = user_session_admin.has_change_permission(None,None)
        self.assertFalse(resultado)


    def test_has_delete_permission(self): 
        user_session_admin = UserSessionAdmin(UserSession,self.admin_site)
        resultado = user_session_admin.has_delete_permission(None,None)
        self.assertFalse(resultado)

class LogRequestAdminTest(TestCase):
    def setUp(self):
        admin_site = AdminSite()
        self.admin_site = admin_site
        
        
    def test_has_add_permission(self): 
        user_session_admin = LogRequestsAdmin(LogRequests,self.admin_site)
        resultado = user_session_admin.has_add_permission(None,None)

        self.assertFalse(resultado)
    def test_has_change_permission(self): 
        user_session_admin = LogRequestsAdmin(LogRequests,self.admin_site)
        resultado = user_session_admin.has_change_permission(None,None)
        self.assertFalse(resultado)


    def test_has_delete_permission(self): 
        user_session_admin = LogRequestsAdmin(LogRequests,self.admin_site)
        resultado = user_session_admin.has_delete_permission(None,None)
        self.assertFalse(resultado)

    def test_get_parametros_vazio(self): 
        user_session_admin = LogRequestsAdmin(LogRequests,self.admin_site)
        resultado = user_session_admin.get_parametros(None)
        self.assertEqual({},resultado)
    
    def test_get_parametros(self): 
        log = LogRequests(
            parametros="""{"next": "/admin/"}"""
        )
        log.save()
        user_session_admin = LogRequestsAdmin(LogRequests,self.admin_site)
        resultado = user_session_admin.get_parametros(log)
        self.assertTrue("pre { width: 450px; } pre" in  resultado)

class PasswordValidationTest(TestCase):
    def setUp(self):
        user = User(name=name, username=username,password=settings.USER_PASSWORD_TEST,is_staff=True)
        user.save()

        self.user = user

    def test_validate_password_with_fusionauth(self):
        settings.USE_FUSIONAUTH = True
        try:
            validate_password(settings.USER_PASSWORD_TEST)
        except ValidationError as e:
            self.fail(f'{e}')

    def test_validate_password(self):
        settings.USE_FUSIONAUTH = False
        try:
            validate_password(settings.USER_PASSWORD_TEST)
        except ValidationError as e:
            self.fail(f'{e}')

    def test_validate_password_invalid(self):
        settings.USE_FUSIONAUTH = False
        with self.assertRaises(ValidationError):
            # senha simples
            validate_password('teste')
        
        with self.assertRaises(ValidationError):
            # com acento
            validate_password('éumteste')
        
        with self.assertRaises(ValidationError):
            # com caracter especial
            validate_password('temespecial!')
        
        with self.assertRaises(ValidationError):
            # com senha antiga
            self.user.set_password('Dpgeceti@20xy')
            self.user.save()
            self.user.set_password(settings.USER_PASSWORD_TEST)
            self.user.save()
            validate_password(settings.USER_PASSWORD_TEST,self.user)
        