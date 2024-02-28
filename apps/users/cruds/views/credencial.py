from apps.core.mixins import GenericCrudAdmin, register
from apps.users.models import CredenciaisUsuario

@register(CredenciaisUsuario)
class CredenciaisUsuarioGenericCrud(GenericCrudAdmin):
    resumo_title_column = 'user'
    model = CredenciaisUsuario
    label = 'Credencial'
    parent_column = 'user'
    list_fields = ('user','sistema','usuario')
    form_fields = ('user','sistema','usuario')
    view_fields = ('user','sistema','usuario')
    