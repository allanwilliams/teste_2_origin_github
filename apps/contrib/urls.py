from apps.contrib.views import municipio, estado, assinatura
from django.urls import path

app_name = 'contrib'

urlpatterns = [
    path("verificar-assinatura", view=assinatura.verificar_assinatura, name="contrib_verificar_assinatura"),
]
