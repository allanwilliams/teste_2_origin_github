from django.test import TestCase, Client
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.models import Group
from apps.contrib.models import Estados
from apps.users.models import User

username = 'teste.user'
name = "Teste User"

class EstadosModelTest(TestCase):
    def setUp(self):
        user = User(name="Teste User", username=username,password=settings.USER_PASSWORD_TEST)
        user.save()
        self.user = user

        estado = Estados(nome="Teste",sigla='Teste')
        estado.save()
        self.estado = estado

    def test_estado_str(self):
        self.assertTrue("Teste" in str(self.estado),self.estado)