from apps.core.mixins import GenericCrudAdmin, register
from apps.contrib.models import Municipios

@register(Municipios)
class MunicipiosGenericCrud(GenericCrudAdmin):
    model = Municipios
    label = 'Municipios'
    parent_column = 'estado'
    list_fields = ('id','nome')
    form_fields= ('estado','nome')
    view_fields=('id','nome')