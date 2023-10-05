from django.contrib.sessions.models import Session
from .models import UserSession

def removerSessao(modeladmin, request, queryset):
    users_selecionados = request.POST.getlist('_selected_action')
    
    for user in users_selecionados:
        print(user)
        user_id = UserSession.objects.filter(id = user)
        print(user_id[0].user_id)
        Session.objects.filter(
            usersession__user=user_id[0].user_id
        ).delete()
removerSessao.short_description = "Deslogar usuário"