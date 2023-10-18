from django.urls import path, include

from apps.users.views import importar_usuarios

app_name = "users"
urlpatterns = [
    path("importar-usuarios", view=importar_usuarios, name="importar_usuarios"),
]
