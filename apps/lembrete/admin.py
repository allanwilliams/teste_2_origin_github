from django.contrib import admin
from django_currentuser.middleware import get_current_user
from django.contrib.admin import SimpleListFilter
from apps.core.mixins import AuditoriaAdmin
from django.utils.html import format_html
from .models import Lembretes
from .forms import LembretesForm
from apps.core.encrypt_url_utils import encrypt, decrypt
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

class OrigemLembreteFilter(SimpleListFilter): # pragma: no cover
    title = 'Origem'
    parameter_name = 'verifica_origem'

    def lookups(self, request, model_admin):
        return (
            ('recebidos', 'Recebidos'),
            ('enviados', 'Enviados'),
        )
    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value() == 'recebidos':
            return queryset.filter(destinatario__id=request.user.id)
        if self.value() == 'enviados':
            return queryset.exclude(destinatario__id=request.user.id)


class DestinatarioFilter(SimpleListFilter): # pragma: no cover
    title = 'Para'
    parameter_name = 'destinatario'

    def lookups(self, request, model_admin):
        result = Lembretes.objects.values_list('destinatario__id','destinatario__name').distinct()
        return ((x[0], x[1].title) for x in result)
    
    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value():
            return queryset.filter(destinatario_id=self.value())

class RemetenteFilter(SimpleListFilter): # pragma: no cover
    title = 'De'
    parameter_name = 'criado_por'

    def lookups(self, request, model_admin):
        result = Lembretes.objects.values_list('criado_por__id','criado_por__name').distinct()
        return ((x[0], x[1].title) for x in result)
    
    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value():
            return queryset.filter(criado_por_id=self.value())
        
@admin.register(Lembretes)
class LembretesAdmin(AuditoriaAdmin): # pragma: no cover

    form = LembretesForm

    change_form_template = 'lembrete_changeform_template.html'

    list_filter = (
        'status',
        'data',
        OrigemLembreteFilter,
        RemetenteFilter,
        DestinatarioFilter,
        'lembrete_proprio'
    )

    search_fields = (
        'titulo',
    )

    list_display = (
        'get_titulo',
        'data',
        'get_origem',
        'get_destino',
        'status',
        'verifica_origem',
        'get_documento'
    )

    readonly_fields = AuditoriaAdmin.readonly_fields + (
        'status',
        'lembrete_proprio'
    )

    fieldsets = (
        ('', {
            'fields': (
                'titulo',
                'destinatario',
                'data',
                'prioridade',
                'descricao',
                'documento'
            ),
        }),
        ('',
            {
                'fields': ('status', 'lembrete_proprio', 'criado_em', 'criado_por', 'modificado_em', 'modificado_por'),
            }),
    )
    
    def get_titulo(self,instance):
        return format_html('<a href="{url}">{text}</a>'.format(url=f'/admin/lembrete/lembretes/{instance.get_encrypt_id()}/change',text=instance.titulo))
    get_titulo.short_description = "Título"


    def change_view(self, request, object_id, form_url='', extra_context=None):
        object_id = decrypt(object_id)
        obj = self.get_object(request, object_id)
        
        if obj is None:
            messages.error(request, "Registro não localizado.")
            return HttpResponseRedirect(reverse('admin:lembrete_lembretes_changelist'))
        
        return super(LembretesAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def get_documento(self, obj):
        if obj.documento:
            diretorio,nome = str(obj.documento).split('/')
            return format_html("<a href='{url}' target='_blank'><i class='fa-solid fa-cloud-arrow-down'></i></a>", url=f'/media/{diretorio}/{encrypt(nome)}')
        else:
            return '-'
    
    get_documento.short_description = "Documento" 

    def get_queryset(self, request):
        from django.db.models import Q
        queryset = super().get_queryset(request)
        current_user = get_current_user()

        if not current_user.is_superuser:
             queryset = queryset.filter(Q(destinatario=current_user.id) | Q(criado_por=current_user.id))
        return queryset


    def has_delete_permission(self, request, obj=None):
        if obj:
            if obj.criado_por.id == get_current_user().id or get_current_user().is_superuser:
                return True
        return False