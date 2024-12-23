from django import forms
from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.contrib.auth.decorators import login_required, permission_required
from django.db import models
from django.forms import Textarea
from django.utils import timezone
from django.shortcuts import render, redirect
from django_currentuser.middleware import get_current_user, get_current_authenticated_user
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse, path
from reversion.admin import VersionAdmin
from apps.core.encrypt_url_utils import encrypt
from apps.core.utils import core_decrypt, core_encrypt,format
from apps.core.permission_functions import permission_required_for_model_view,permission_required_for_user_view
from reversion import register
from reversion.revisions import is_active, set_comment
import reversion
import json
import decimal
import inspect

LIST_PER_PAGE = 10

@register
class BaseModel(models.Model):
    criado_em = models.DateTimeField(blank=True, null=True)
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.DO_NOTHING,
                                   related_name='%(class)s_criado_por',
                                   blank=True,
                                   null=True,
                                   default=get_current_user())
    modificado_em = models.DateTimeField(blank=True, null=True)
    modificado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       on_delete=models.DO_NOTHING,
                                       related_name='%(class)s_modificado_por',
                                       blank=True,
                                       null=True)

    crypted_fields = []
    masked_fields = []

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        original = self._meta.model.objects.filter(pk=self.pk).first()
            
        if get_current_authenticated_user():
            if self.pk is None:
                if not self.criado_por or not self.criado_em:
                    self.criado_por = get_current_authenticated_user()
                    self.criado_em = timezone.now()
            elif original:
                    self.modificado_por = get_current_authenticated_user()
                    self.modificado_em = timezone.now()
                    self.criado_em = original.criado_em
                    self.criado_por = original.criado_por
        
        for crypted_field in self.crypted_fields:
            new_value = core_encrypt(getattr(self, crypted_field))
            setattr(self, crypted_field, new_value)
        
        with reversion.create_revision():
            comment = []
            if original and self._meta.model_name not in ['userpage', 'usersession']:
                try:
                    changed_fields = []
                    for field in self._meta.fields:
                        field_name = f'{field.name}_id' if isinstance(field, models.ForeignKey) else field.name
                        if field_name not in ['criado_por_id', 'criado_em', 'modificado_por_id', 'modificado_em']:
                            field_value = getattr(self, field_name)
                            original_value = getattr(original, field_name)
                            if field_value != original_value:
                                changed_fields.append(field_name)
                    
                    if len(changed_fields) > 0:
                        comment = [{"changed": {"name":self._meta.verbose_name,"object": str(self),"fields": changed_fields}}]
                except Exception as e:
                    pass                
            else:
                if self._meta.model_name not in ['userpage', 'usersession']:
                    try:
                        comment = [{"added": {"name":self._meta.verbose_name,"object": str(self)}}]
                    except:
                        comment = [{"added": {"name":self._meta.verbose_name,"object": ''}}]

            reversion.set_comment(json.dumps(comment))
            reversion.set_user(get_current_authenticated_user())
            super(BaseModel, self).save(*args, **kwargs)
    
    def get_encrypt_id(self):
        return encrypt(self.id)
    
    @classmethod
    def from_db(cls, db, field_names, values):
        for crypted_field in cls.crypted_fields:
            index = field_names.index(crypted_field)
            new_value = core_decrypt(values[index])
            new_values = list(values)
            new_values[index] = new_value
            values = tuple(new_values)
        return super().from_db(db, field_names, values)
    
    def can_edit_crud(self):
        current_user = get_current_authenticated_user()
        if current_user.has_perm(f'{self._meta.app_label}.change_{self._meta.model_name}'):
            return True
        
        return False
    
    def can_delete_crud(self):
        current_user = get_current_authenticated_user()
        if current_user.has_perm(f'{self._meta.app_label}.delete_{self._meta.model_name}'):
            return True
        
        return False
    
    def can_add_crud(self):
        current_user = get_current_authenticated_user()
        if current_user.has_perm(f'{self._meta.app_label}.add_{self._meta.model_name}'):
            return True
        
        return False

    def can_view_crud(self):
        current_user = get_current_authenticated_user()
        if current_user.has_perm(f'{self._meta.app_label}.view_{self._meta.model_name}'):
            return True
        
        return False


class BaseModelDRF(models.Model):
    criado_em = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.DO_NOTHING,
                                   related_name='%(class)s_criado_por',
                                   blank=True,
                                   null=True)
    modificado_em = models.DateTimeField(blank=True, null=True, auto_now=True)
    modificado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       on_delete=models.DO_NOTHING,
                                       related_name='%(class)s_modificado_por',
                                       blank=True,
                                       null=True)

    class Meta:
        abstract = True


class AuditoriaAdmin(VersionAdmin):
    # def changelist_view(self, request, extra_context=None):
    #     response = super().changelist_view(request, extra_context=extra_context)
    #     result_list = response.context_data['cl'].result_list
    #     if self.model.masked_fields:
    #         for obj in result_list:
    #             for field in self.model.masked_fields:
    #                 setattr(obj,field,eval(self.model.masked_fields[field]['function'])(getattr(obj,field),''))
        
    #     response.context_data['cl'].result_list = result_list

    #     return response

    def log_change(self, request, object, message):
        entry = super().log_change(request, object, message)
        if is_active():
            set_comment(entry.change_message)
        return entry


    def log_addition(self, request, object, message):
        change_message = message or ("Initial version.")
        entry = super().log_addition(request, object, change_message)
        if is_active():
            set_comment(entry.change_message)
        return entry

    readonly_fields = (
        'criado_em',
        'criado_por',
        'modificado_em',
        'modificado_por',
    )
    list_per_page = LIST_PER_PAGE


class AuditoriaAdminInline(admin.TabularInline):
    readonly_fields = (
        'criado_em',
        'criado_por',
        'modificado_em',
        'modificado_por',
    )
    list_per_page = LIST_PER_PAGE
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea(attrs={
                'rows': 8,
                'cols': 40
            })
        },
        models.ForeignKey: {
            # 'widget': Select(attrs={'style': 'max-width: 150px'})
        },
        models.CharField: {
            # 'widget': TextInput(attrs={'style': 'max-width: 150px'})
        },
    }

class AuditoriaAdminStackedInlineInline(admin.StackedInline):
    readonly_fields = (
        'criado_em',
        'criado_por',
        'modificado_em',
        'modificado_por',
    )
    list_per_page = LIST_PER_PAGE


class BooleanDefaultNoFilter(SimpleListFilter):

    def lookups(self, request, model_admin):
        return (
            ('tudo', 'Tudo'),
            ('sim', 'Sim'),
            ('nao', 'Não'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'nao':
            dic = {self.parameter_name: False}
            return queryset.filter(**dic)
        elif self.value() == 'sim':
            dic = {self.parameter_name: False}
            return queryset.exclude(**dic)
        return queryset

class DecimalEncoder(json.JSONEncoder):
    def default(self, item):
        if isinstance(item, decimal.Decimal):
            return float(item)
        return super(DecimalEncoder, self).default(item)

def compact(*names):
    caller = inspect.stack()[1][0]
    result = {}

    for n in names:
        if n in caller.f_locals:
            result[n] = caller.f_locals[n]
        elif n in caller.f_globals:
            result[n] = caller.f_globals[n]
    return result

_models_crud_registry = {}

def get_urls():
    '''
        cria urls dos cruds genéricos
    '''
    
    urls = []
    for model, model_admin in _models_crud_registry.items():
        model_name = model_admin.model._meta.model_name
        app_label = model_admin.model._meta.app_label
        urls_model = [
            path(f"{app_label}/{model_name}-criar/", model_admin.criar, name=f'{app_label}_{model_name}_criar'),
            path(f"{app_label}/{model_name}-criar/<parent_id>/", model_admin.criar, name=f'{app_label}_{model_name}_criar'),

            path(f"{app_label}/{model_name}-visualizar/<pk>/<parent_id>/", model_admin.visualizar, name=f'{app_label}_{model_name}_visualizar'),
            path(f"{app_label}/{model_name}-visualizar/<pk>/", model_admin.visualizar, name=f'{app_label}_{model_name}_visualizar'),

            path(f"{app_label}/{model_name}-editar/<pk>/<parent_id>/", model_admin.editar, name=f'{app_label}_{model_name}_editar'),
            path(f"{app_label}/{model_name}-editar/<pk>/", model_admin.editar, name=f'{app_label}_{model_name}_editar'),

            path(f"{app_label}/{model_name}-excluir/<pk>/<parent_id>/", model_admin.excluir, name=f'{app_label}_{model_name}_excluir'),
            path(f"{app_label}/{model_name}-excluir/<pk>/", model_admin.excluir, name=f'{app_label}_{model_name}_excluir'),
        ]

        if model_admin.is_parent:
            urls = urls + [
                path(f"{app_label}/{model_name}-show/<pk>/", model_admin.show_pai, name=f'{app_label}_{model_name}_show'),
            ]
        urls += urls_model
    return urls

class GenericCrudAdmin():
    '''
        Constrói classe admin do Crud Genérico
        instance = instancia do objeto
        resumo = uma tupla contendo as colunas que irão aparecer na tela do pai
        resumo_title_column = desabilitada
        is_parent = informa se o crud gerado possui filhos (ex: processos possuem atividades/agendamentos...)
        tabs = recebe um array com as tabs do pai (as tabs são heranças de <GenericCrudTab>)
        is_many = desabilitada
        model = model que será usada no crud
        label = Identifica a model (utilizado para mensagens de alerta no sistema e na apresentação de dados em tela)
        list_fields = desabilitada
        form_fields = fields que irão compor a construção do formulario genérico
        view_fields = fields que serão exibidos na tela de visualizar do crud genérico
        parent_column = coluna que estabelece a relação entre pai e filho
        form = o formulário do crud pode ser sobreescrito
        modais_visualizar = actions e/ou modais que serão incorporados na tela do show pai
        modais_editar = actions e/ou modais que serão incorporados na tela de edição
        modais_criar = actions e/ou modais que serão incorporados na tela de criação
        url_externaurl_externa = usada no historico padrão. Consultar contrução do historico
        template_lista_item = usada no historico padrão. Consultar contrução do historico
        template_header = usada no historico padrão. Consultar contrução do historico
        disable_actions = se True desabilita os botões de edição do pai e dos filhos

        view_template = template da tela de view
        add_template = template da tela de add
        edit_template = template da tela de edit
        show_template = template da tela do pai
    '''
    instance = None
    resumo = None
    resumo_title_column = None
    is_parent = False
    tabs = None
    is_many = False
    model = None
    label = None
    list_fields = ()
    form_fields = ()
    view_fields = ()
    parent_column = None
    form = None
    _registry = {}
    modais_visualizar = []
    modais_editar = []
    modais_criar = []
    actions_top_bar = []
    url_externa = None
    template_lista_item = None
    template_header = None
    disable_actions = False

    view_template = 'generic_crud/generic_visualizar.html'
    add_template = 'generic_crud/generic_criar.html'
    edit_template = 'generic_crud/generic_editar.html'
    show_template = 'generic_crud/parent_visualizar.html'
    
    def validar_acesso(self):
        current_user = get_current_authenticated_user()
        if not current_user:
            return redirect('/admin/login/')
        return True

    def visualizar(self,request, pk, parent_id=None,extra_context=None):
        nao_autenticado = self.validar_acesso()

        if isinstance(nao_autenticado,HttpResponseRedirect):
            return nao_autenticado
        
        parent_class = None
        if self.parent_column:
            parent_class = self.get_parent_class(self)
        instance_object = self.verify_element_exists(request,pk)

        # caso a instance não seja da model do crud irá retornar para o redirect enviado por verify_element_exists
        if isinstance(instance_object,HttpResponseRedirect):
            return instance_object
                    
        context = {
            'instance_object': instance_object,
            'crud': self,
            **(extra_context or {}),
        }
        
        if parent_id and parent_class and self.parent_column:
            context['parent_id'] = parent_id
            context['parent_object'] = parent_class.objects.get(pk=parent_id)
            context['back_url'] = f'/{parent_class._meta.app_label}/{parent_class._meta.model_name}-show/{parent_id}'

        return render(request, self.view_template, context)
    
    def criar(self,request,parent_id=None,extra_context=None):
        nao_autenticado = self.validar_acesso()

        if isinstance(nao_autenticado,HttpResponseRedirect):
            return nao_autenticado
        
        CRIADO_SUCESSO = f'{self.label} criado(a) com sucesso!'
        ERRO_INTERNO = f'Erro interno ao criar {self.label}!'
        parent_class = None
        if self.parent_column:
            parent_class = self.get_parent_class(self)
        form = self.get_form()

        if request.method == 'POST':
            form = form(request.POST, request.FILES)
            
            if form.is_valid():
                try:
                    instance_object = form.save()
                    if request.is_ajax(): # pragma: no cover
                        return HttpResponse(json.dumps({'mensagem': CRIADO_SUCESSO}), status=200, content_type="application/json")
                except Exception: # pragma: no cover
                    return HttpResponse(json.dumps({'mensagem': ERRO_INTERNO}), status=500, content_type="application/json")
                
                messages.success(request, CRIADO_SUCESSO)
                if self.parent_column and parent_id:
                    return redirect(f'/{parent_class._meta.app_label}/{parent_class._meta.model_name}-show/{parent_id}')
                else:
                    return redirect(f'/{self.model._meta.app_label}/{self.model._meta.model_name}-show/{instance_object.id}')
            else:
                if request.is_ajax(): # pragma: no cover
                    errors = dict(form.errors.items())
                    return HttpResponse(json.dumps(errors), status=400, content_type="application/json")
        
        context = {
            'form': form,
            'parent_id': parent_id,
            'crud': self,
            **(extra_context or {}),
        }

        if parent_id and parent_class and self.parent_column:
            context['parent_object'] = parent_class.objects.get(pk=parent_id)
            context['back_url'] = f'/{parent_class._meta.app_label}/{parent_class._meta.model_name}-show/{parent_id}'

        return render(request, self.add_template, context)

    def editar(self,request, pk,parent_id=None,extra_context=None):
        nao_autenticado = self.validar_acesso()

        if isinstance(nao_autenticado,HttpResponseRedirect):
            return nao_autenticado
        
        EDITADO_SUCESSO = f'{self.label} editado(a) com sucesso!'
        ERRO_EDITAR = f'Erro ao editar {self.label}!'
        parent_class = None
        if self.parent_column:
            parent_class = self.get_parent_class(self)
        instance_object = self.verify_element_exists(request,pk)
        
        # caso a instance não seja da model do crud irá retornar para o redirect enviado por verify_element_exists
        if isinstance(instance_object,HttpResponseRedirect):
            return instance_object
        
        form = self.get_form()
        form = form(request.POST or None, request.FILES or None, instance=instance_object)
        
        if request.method == 'POST' and form.is_valid():
            try:
                form.save()
                messages.success(request, EDITADO_SUCESSO)
            except Exception: # pragma: no cover
                if request.is_ajax(): # pragma: no cover
                    return HttpResponse(json.dumps(dict(form.errors.items())), status=400, content_type='application/json')        
                messages.error(request, ERRO_EDITAR)
            if self.parent_column and parent_id:
                return redirect(f'/{parent_class._meta.app_label}/{parent_class._meta.model_name}-show/{parent_id}')
            else:
                return redirect(f'/{self.model._meta.app_label}/{self.model._meta.model_name}-editar/{instance_object.id}')
        else:
            if request.is_ajax():# pragma: no cover
                errors = dict(form.errors.items())
                return HttpResponse(json.dumps(errors), status=400, content_type="application/json")

        context = {
            'parent_id': int(parent_id) if parent_id else parent_id,
            'form': form,
            'instance_object': instance_object,
            'crud': self,
            **(extra_context or {}),
        }

        if parent_id and parent_class and self.parent_column:
            context['parent_object'] = parent_class.objects.get(pk=parent_id)
            context['back_url'] = f'/{parent_class._meta.app_label}/{parent_class._meta.model_name}-show/{parent_id}'

        return render(request, self.edit_template, context)

    def excluir(self, request, pk, parent_id=None,extra_context=None):
        nao_autenticado = self.validar_acesso()

        if isinstance(nao_autenticado,HttpResponseRedirect):
            return nao_autenticado
        
        parent_class = None
        if self.parent_column:
            parent_class = self.get_parent_class(self)

        instance_object = self.model.objects.filter(pk=pk).first()
        
        if instance_object:
            try:
                instance_object.delete()
                messages.success(request, f'{self.label} removido com sucesso!')
            except Exception: # pragma: no cover
                messages.error(request, f'Não foi possivel remover a {self.label}!')

        if self.parent_column and parent_id and self.parent_column:
            return redirect(f'/{parent_class._meta.app_label}/{parent_class._meta.model_name}-show/{parent_id}')
        
    def show_pai(self, request, pk,extra_context=None):
        nao_autenticado = self.validar_acesso()

        if isinstance(nao_autenticado,HttpResponseRedirect):
            return nao_autenticado
        
        from apps.core.helpers.historico_padrao import get_historico
        EDITADO_SUCESSO = f'{self.label} editado(a) com sucesso!'
        ERRO_EDITAR = f'Erro ao editar {self.label}!'
        
        instance_object = self.verify_element_exists(request,pk)
        # caso a instance não seja da model do crud irá retornar para o redirect enviado por verify_element_exists
        if isinstance(instance_object,HttpResponseRedirect):
            return instance_object
        
        self.instance = instance_object
        form = self.get_form()
        form = form(request.POST or None, request.FILES or None, instance=instance_object)
        if request.method == 'POST' and form.is_valid():
            try:
                form.save()
                messages.success(request, EDITADO_SUCESSO)
            except Exception: # pragma: no cover
                if request.is_ajax(): # pragma: no cover
                    return HttpResponse(json.dumps(dict(form.errors.items())), status=400, content_type='application/json')        
                messages.error(request, ERRO_EDITAR)
            
            return redirect(f'/{self.model._meta.app_label}/{self.model._meta.model_name}-show/{pk}')
        
        historico = get_historico(
            id=[pk], 
            eventos=['added','changed'], 
            model_app=self.model, 
            campos_bloqueados=['num_processo'], 
            extra_data=[]
        )

        historico_padrao = {
            'dados': historico,
            'header': 'Movimentações Principais',
            'url_externa': self.url_externa,
            'template_lista_item': self.template_lista_item,
            'template_header': self.template_header,
            'dados_header': [
                {'label': 'Defensor(a)', 'cor': 'bg-verde'},
                {'label': 'Estagiário(a)', 'cor': 'bg-roxo'},
                {'label': 'Colaborador(a)', 'cor': 'bg-amarelo'},
                {'label': 'Assessor(a)', 'cor': 'bg-azul'},
            ]
        }

        context = {
            'object_id': pk,
            'instance_object': instance_object,
            'parent_object': instance_object,
            'form': form,
            'crud': self,
            'historico_padrao': historico_padrao,
            'tabs': [],
            **(extra_context or {}),
        }
        if len(self.tabs) > 0:
            for tab in self.tabs:
                tab_models = []
                for tab_model in tab.models:
                    tab_objects = tab_model.model.objects.filter(**{tab_model.parent_column:pk})
                    tab_models.append({
                        'self_tab':tab_model,
                        'tab_model':tab_model.model,
                        'objects': tab_objects
                    })
                context['tabs'].append(tab_models)
                historico_tab = get_historico(
                    id=[tab.id for tab in tab_objects], 
                    eventos=['added','changed'], 
                    model_app=tab_model.model, 
                    campos_bloqueados=['num_processo'], 
                    extra_data=context['historico_padrao']['dados']
                )
                context['historico_padrao']['dados'] = historico_tab
        
        return render(request, self.show_template, context)
    
    def get_form(self):
        if self.form:
            if self.form_fields:
                self.form.Meta.fields = self.form_fields
            else:
                self.form.Meta.fields = self.fields

            return self.form

        crud = self
        class Meta:
            model = self.model
            fields = self.get_form_fields()
            if self.parent_column:
                fields.append(self.parent_column)
            label_form = self.label

        def __init__(self, *args, **kwargs):
            super(GenericForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                try:
                    self.fields[field].widget.attrs['class'] = crud.get_field_default_class(field)
                except: pass

            
        # Cria uma nova classe de formulário usando type
        GenericForm = type('GenericForm', (forms.ModelForm,), {'Meta': Meta,'__init__': __init__})

        return GenericForm

    @property
    def fields(self):
        return self.get_form_fields()
    
    def get_form_fields(self):
        if self.form_fields:
            return list(self.form_fields)
        fields = []
        for field in self.model._meta.fields:
            if field.name not in ['criado_em','criado_por','atualizado_em','atualizado_por']:
                fields.append(field.name)
        return fields

    # def get_form_field_class(self):
    #     if self.form_fields:
    #         return self.form_fields
        
    #     fields = {}
    #     for field in self.model._meta.fields:
    #         if field.name not in ['criado_em','criado_por','atualizado_em','atualizado_por']:
    #             fields[field.name] = None
    #     return fields

    def get_parent_class(self, crud):
        return crud.model._meta.get_field(crud.parent_column).related_model
    
    def verify_element_exists(self,request,pk):
        instance_object = self.model.objects.filter(pk=pk).first()
        if instance_object:
            return instance_object
        
        msg_erro_inexistente = f"O {self.label} com ID “{pk}” não existe. Talvez tenha sido deletado."
        messages.error(request, msg_erro_inexistente)
        return redirect('/admin/')
    
    def get_field_default_class(self,field):
        field_type = self.model._meta.get_field(field).__class__.__name__
        class_field = 'vTextField'

        if field_type == 'DateField':
            class_field = 'vDateField datepicker '

        if field_type == 'TextField':
            class_field = 'vLargeTextField nossa-textarea'
        
        return class_field

class GenericCrudTab():
    models = None

class GerericCrudTabModel():
    '''
        model = Model da tab
        tab_fields = lista de fields que serão apresentados na lista de registros da tab
        parent_column = coluna que estabelece a relação entre pai e filho
        model_name = Nome da model (será utilizada para gerar o ID da tab dentro do show do pai)
        action_buttons = se False os botões de action da tab serão removidos
    '''
    model = None
    tab_fields = None
    parent_column = None
    model_name = None
    action_buttons = True

def register(*models, site=None):
    def _model_admin_wrapper(admin_class):
        if not models:
            raise ValueError('At least one model must be passed to register.')

        if not issubclass(admin_class, GenericCrudAdmin):
            raise ValueError('Wrapped class must subclass GenericCrudAdmin.')

        _models_crud_registry[models] = admin_class()
    return _model_admin_wrapper    