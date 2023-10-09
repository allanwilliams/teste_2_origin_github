from django.test import TestCase
from apps.users.models import User,UserPreferencias, Defensores, Papeis, DefensoresLotacoes
from apps.users.forms import UserCreationForm, UserChangeForm
from django.conf import settings

class UserModelTest(TestCase):
    def setUp(self):
        user = User(name="Teste User", username='teste.user',password='Dpgeceti@20xx')
        user.save()
        self.user = user

        papel = Papeis(id=1,titulo='Defensor')
        papel.save()

        user_defensor = User(name="Teste", username='teste.user.defensor', papel=papel)
        user_defensor.save()

        self.user_defensor = user_defensor

    def test_user_str(self):
        self.assertTrue("Teste User (teste.user)" in str(self.user))

    def test_get_preferencia(self):
        preferencia = UserPreferencias(user=self.user, preferencia=1)
        preferencia.save()

        prefencias = self.user.get_user_preferencias()
        self.assertTrue(len(prefencias) > 0,'Preferências do usuário não carregadas')

    def test_validated_is_defensor(self):
        self.assertTrue(self.user_defensor.is_defensor())
    
    def test_validated_is_not_defensor(self):
        self.assertFalse(self.user.is_defensor())

    def test_troca_senha_usuario(self):
        settings.USE_FUSIONAUTH = False
        self.user.set_password('Dpgeceti@20yy')
        self.user.save()

        self.assertTrue(self.user.check_password('Dpgeceti@20yy'))


class UserFormTest(TestCase):
    def setUp(self):
        user = User(first_name="Teste", last_name="Init", username='teste.init',cpf='00000000000')
        user.save()
        self.user = user

    def test_valid_data(self):
        form = UserCreationForm({
            'username':'teste.user',
            'password1': 'Dpgeceti@20xx',
            'password2': 'Dpgeceti@20xx',
        })

        self.assertTrue(form.is_valid())

        usuario = form.save()
        self.assertTrue("(teste.user)" in str(usuario),str(usuario))

    def test_duplicated_username(self):
        create_user_form = UserCreationForm({
            'username':'teste.user',
            'password1': 'Dpgeceti@20xx',
            'password2': 'Dpgeceti@20xx',
        })

        create_user_form.is_valid()

        create_user_form.save()

        change_user_form = UserChangeForm({
            'cpf': '00000000000'
        })

        self.assertFalse(change_user_form.is_valid())

    def test_duplicated_cpf(self):
        form1 = UserCreationForm({
            'username':'teste.user',
            'password1': 'Dpgeceti@20xx',
            'password2': 'Dpgeceti@20xx',
        })

        form1.is_valid()

        form1.save()

        form2 = UserCreationForm({
            'username':'teste.user',
            'password1': 'Dpgeceti@20xx',
            'password2': 'Dpgeceti@20xx',
        })

        self.assertFalse(form2.is_valid())

class PapeisModelTest(TestCase):
    def setUp(self):
        papel = Papeis(id=1,titulo='Defensor')
        papel.save()
        self.papel = papel

    def test_papel_str(self):
        self.assertTrue('Defensor',str(self.papel))

class DefensorModelTest(TestCase):
    def test_defensor_str(self):
        user = User(first_name="Teste", last_name="User", username='teste.user')
        user.save()

        defensor = Defensores(nome='teste',matricula='0000',cpf='00000000000',user=user)
        defensor.save()
        self.assertEquals(str(defensor),defensor.nome)

class DefensoresLotacoesModelTest(TestCase):
    def setUp(self):
        from datetime import datetime
        defensor_lotacao = DefensoresLotacoes(
            defensor_nome='teste',
            defensoria='teste defensoria',
            origem_id=1,
            data_inicio=datetime.today()
        )
        defensor_lotacao.save()

        self.defensor_lotacao = defensor_lotacao
    
    def test_defensores_lotacoes_str(self):
        self.assertEqual('teste - teste defensoria',str(self.defensor_lotacao))
