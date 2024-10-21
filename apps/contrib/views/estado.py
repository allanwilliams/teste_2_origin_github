from apps.core.mixins import GenericCrudAdmin,GenericCrudTab,GerericCrudTabModel, register
from apps.contrib.models import Estados, Municipios

class MunicipiosTab(GenericCrudTab):
    class MunicipiosTabModel(GerericCrudTabModel):
        model = Municipios
        tab_fields = ['nome','estado']
        parent_column = 'estado'
        tab_name = 'Municipios'
        model_name = 'Municipios'

    models = [MunicipiosTabModel]

@register(Estados)
class EstadoGenericCrud(GenericCrudAdmin):
    resumo = [
        ('nome',),
    ]
    tabs = [MunicipiosTab,]
    resumo_title_column = 'nome'
    model = Estados
    label = 'Estados'
    list_fields = ('id','nome')
    form_fields = ('id','nome','sigla')
    view_fields = ('id','nome')
    is_parent = True
    parent_column = 'id'