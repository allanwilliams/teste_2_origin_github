from django.db import models
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)
from apps.core.mixins import BaseModel
from apps.users.models import User
from django.contrib.sessions.models import Session
from django.conf import settings
from django.contrib.auth import user_logged_in, user_login_failed
import django.contrib.auth as dAuth
from django.dispatch.dispatcher import receiver
from datetime import datetime,timedelta
from django.contrib import messages
from django.utils.html import format_html

def _update_session_auth_hash(request, user):
    """
    Updating a user's password logs out all sessions for the user.

    Take the current request and the updated user object from which the new
    session hash will be derived and update the session hash appropriately to
    prevent a password change from logging out the session from which the
    password was changed.
    """
    if hasattr(user, 'get_session_auth_hash') and request.user == user:
        request.session.cycle_key()
        request.session['_auth_user_hash'] = user.get_session_auth_hash()
        user_logged_in.send(sender=user.__class__, request=request, user=user)

dAuth.update_session_auth_hash = _update_session_auth_hash

class LogRequests(models.Model):
    cols = {
        'url': 2,
    }
    user = models.ForeignKey(
        User, 
        related_name='%(class)s_usersession',
        on_delete=models.DO_NOTHING,
        verbose_name='Usuário',
        null=True,
        blank=True
    )
    session_key = models.CharField(max_length=300,null=True,blank=True)
    ip = models.CharField(max_length=20,null=True,blank=True)
    ip_publico = models.CharField(max_length=20,null=True,blank=True)
    navegador = models.CharField(max_length=300,null=True,blank=True)
    url = models.CharField(max_length=300,null=True,blank=True)
    url_atual = models.CharField(max_length=500,null=True,blank=True)
    data_hora = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    metodo  = models.CharField(max_length=10,null=True,blank=True)
    parametros  = models.TextField(null=True,blank=True)
    response = models.TextField(null=True,blank=True)
    tempo = models.FloatField(null=True,blank=True)

class UserSession(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "usuário online"
        verbose_name_plural = "Usuários online"
        
    @receiver(user_logged_in)
    def remover_sessao(sender, user, request, **kwargs):
        user.num_tentativa_acesso = 0
        user.save()
        Session.objects.filter(
            usersession__user=user
        ).delete()
        request.session.save()
        UserSession.objects.get_or_create(
            user=user,
            session_id=request.session.session_key
        )
    
    @receiver(user_login_failed)
    def block_user(sender, credentials, request, **kwargs):
        user = User.objects.filter(username=credentials['username']).first()
        MUM_TENTATIVA_BLOCK = 10
        if user:
            user.num_tentativa_acesso = user.num_tentativa_acesso + 1
            user.save()
            if user.num_tentativa_acesso >= 2:
                TENTATIVA_RESTANTE = MUM_TENTATIVA_BLOCK - user.num_tentativa_acesso
                messages.add_message(request, messages.ERROR,"Sucessivas tentativas de login sem sucesso!")
                messages.add_message(request, messages.ERROR,format_html(f"Você possui <strong>{TENTATIVA_RESTANTE} tentativas restantes</strong>"))
            if user.num_tentativa_acesso == 9:
                TENTATIVA_RESTANTE = MUM_TENTATIVA_BLOCK - user.num_tentativa_acesso       
                messages.add_message(request, messages.ERROR,"Seu usuário será bloqueado na próxima tentativa!")
            if user.num_tentativa_acesso >= 10:
                user.is_active = False
                user.num_tentativa_acesso = 0
                user.save()
                messages.add_message(request, messages.ERROR,f"Usuário bloqueado por múltiplas tentativas de acesso incorretas! Favor entrar em contato com a equipe de suporte")
        
    def time_online(self):
        me = self.modificado_em if self.modificado_em is not None else datetime.now() - timedelta(minutes=6)
        final = datetime.now() - timedelta(minutes=5)
        
        return False if me < final  else True
    
class UserPage(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    url = models.CharField('url', max_length=500)
    
    class Meta:
        verbose_name = "usuário página"
        verbose_name_plural = "Usuários página"
        
    def time_online(self):
        me = self.modificado_em if self.modificado_em is not None else datetime.now() - timedelta(minutes=6)
        final = datetime.now() - timedelta(minutes=5)
        
        return False if me < final  else True
    

