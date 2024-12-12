from apps.core.mixins import GenericCrudAdmin,GenericCrudTab,GerericCrudTabModel, register
from apps.users.models import User,CredenciaisUsuario

class CredenciaisUsuarioTab(GenericCrudTab):
    class CredenciaisUsuarioTabModel(GerericCrudTabModel):
        model = CredenciaisUsuario
        tab_fields = ['user','sistema','usuario']
        parent_column = 'user'
        tab_name = 'Credenciais'
        model_name = 'CredenciaisUsuario'

    models = [CredenciaisUsuarioTabModel]

@register(User)
class UserGenericCrud(GenericCrudAdmin):
    resumo = [
        ('name',),
    ]
    tabs = [CredenciaisUsuarioTab]
    resumo_title_column = 'name'
    model = User
    label = 'Usuário'
    list_fields = ('name','matricula')
    form_fields = ('name','matricula')
    view_fields = ('name','matricula')
    is_parent = True