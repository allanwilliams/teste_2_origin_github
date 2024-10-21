from django.apps import apps
import json
from django.contrib.contenttypes.models import ContentType
from reversion.models import Version as ReversionVersion
from apps.core.helpers.string import strip_tags
from django.conf import settings  
from apps.users.models import User

tipo_events = {
    'added': 'Adicionou',
    'changed': 'Alterou',
    'deleted': 'Deletou',
    'reverted': 'Revertido',
    'legacy': 'Legado'
}

def get_historico(id, model_app, eventos=['added', 'changed', 'deleted', 'reverted', 'legacy'], campos_bloqueados = [], extra_data = [],filter_column=None):
    model_content_type = ContentType.objects.get_for_model(model_app)
    versoes_default = ReversionVersion.objects.filter(object_id__in=id,content_type_id=model_content_type.id)
    historico = []

    historico = get_historico_versao(versoes_default,eventos,filter_column,campos_bloqueados,model_app)
    
    historico = historico + extra_data
    historico = [dict(t) for t in {tuple(d.items()) for d in historico}]
    historico = sorted(historico, key=lambda x:(x['criado_em']), reverse=True)
    return historico

def get_historico_versao(versoes,eventos,filter_column,campos_bloqueados,model_app,log=False):
    historico = []
    revisions = []
    for versao in versoes:
        serialized_data = json.loads(versao.serialized_data)[0]
        comments = []
        filter_revision = list(filter(lambda rev: rev['revision_id'] == versao.revision_id, revisions))
        if filter_revision:
            revision = filter_revision[0]['revision_data']
        else:
            revision = versao.revision
            revisions.append({
                'revision_id': revision.id,
                'revision_data': revision
            })
        
        try:
            if filter_column and filter_column in revision.comment:
                comments = json.loads(revision.comment)
            else:
                comments = json.loads(revision.comment)
        except Exception as e:
            str_acao = 'legacy'

            if 'Revertido' in revision.comment:
                str_acao = 'reverted'

            if revision.comment != 'Adicionado.':
                comments = [{str_acao: {'name': revision.comment, 'object': '' }}]
        for acao in comments:
            for event in eventos:
                if acao.get(event):
                    mudancas = acao.get(event)
                    if event == 'added' or event == 'deleted' or event == 'reverted' or event == 'legacy':
                        user = revision.user if revision.user_id else None
                        if user and not user.papel:
                            user = User.objects.get(pk=user.id)
                        data_modificacao = revision.date_created
                        historico.append({
                            'usuario': user.name if user.name else 'Sistema',
                            'usuario_papel': str(user.papel) if user.papel else 'Sistema',
                            'evento': tipo_events.get(event),
                            'tipo': mudancas.get('name'),
                            'verbose': mudancas.get('name'),
                            'referencia': mudancas.get('object'),
                            'criado_em': data_modificacao
                        })
                    else:
                        if mudancas.get('name') and mudancas.get('name') == model_app._meta.verbose_name:
                            if filter_column and filter_column not in mudancas:
                                continue
                            historico = historico + get_inline_data(
                                object_repr = mudancas.get('object'),
                                revision_id = versao.revision_id,
                                user = revision.user,
                                campos_bloqueados = campos_bloqueados,
                                mudancas = mudancas,
                                event = event,
                                log=log
                            )
                        else:
                            user = revision.user if revision.user_id else None
                            if user and not user.papel:
                                user = User.objects.get(pk=user.id)
                            data_modificacao = revision.date_created
                            campos = mudancas.get('fields')
                            if campos:
                                for campo in campos:
                                    try:
                                        if campo not in campos_bloqueados:
                                            if filter_column and filter_column != campo:
                                                continue

                                            field = model_app._meta.get_field(campo)
                                            
                                            value_campo = serialized_data.get('fields').get(campo)
                                            if field.related_model:
                                                value_campo = field.related_model.objects.filter(id=value_campo).first()

                                            if field.choices:
                                                    for chave, descricao in field.choices:
                                                        if value_campo == chave:
                                                            value_campo = descricao
                                            
                                            value_campo = strip_tags(str(value_campo)).strip() if value_campo else value_campo
                                            if not value_campo or value_campo == '':
                                                value_campo = 'Vazio'
                                            
                                            if field_is_sigiloso(model_app,versao.object_id,campo):
                                                value_campo = '*** Esta observação/anotação é sigilosa ***'
                                                
                                            hist = {
                                                'usuario': user.name if user.name else 'Sistema',
                                                'usuario_papel': str(user.papel) if user.papel else 'Sistema',
                                                'evento': tipo_events.get(event),
                                                'tipo': model_app._meta.verbose_name.title(),
                                                'verbose': model_app._meta.verbose_name.title(),
                                                'campo': field.verbose_name,
                                                'valor': value_campo,
                                                'criado_em': data_modificacao
                                            }
                                            if hist not in historico:
                                                historico.append(hist)
                                    except Exception as e: 
                                        pass
    
    return historico
def get_inline_data(
    object_repr, #str do objeto
    revision_id, #id da revisao
    user, 
    campos_bloqueados, #campos que não devem entrar no array
    mudancas, #
    event,
    referencia = None,log=False):
    
    model_version = ReversionVersion 
    versao_inline = model_version.objects.filter(object_repr=object_repr,revision_id=revision_id).first()
    historico_inline = []
    if versao_inline:
        data_modificacao = versao_inline.revision.date_created
        campos = mudancas.get('fields')
        if campos:
            inline_serialized_data = json.loads(versao_inline.serialized_data)[0]
            app_label, model_name = inline_serialized_data.get('model').split('.')
            model = apps.get_model(app_label=app_label, model_name=model_name)
            for campo in campos:
                if campo not in campos_bloqueados:
                    try:
                        field = model._meta.get_field(campo)
                        value_campo = inline_serialized_data.get('fields').get(campo)
                        if field.is_relation and field.related_model:
                            try:
                                ids_relateds = inline_serialized_data.get('fields').get(campo)
                                value_campo = field.related_model.objects.filter(id__in=ids_relateds).first()
                            except:
                                try:
                                    campo_editado = campo.split('_id')[0]
                                    ids_relateds = inline_serialized_data.get('fields').get(campo_editado)
                                    value_campo = field.related_model.objects.filter(id__in=[ids_relateds]).first()
                                except: pass
                        if field.choices:
                            value_campo = list(filter(lambda choice: choice[0] == value_campo,field.choices))[0][1]

                        value_campo = strip_tags(str(value_campo)).strip() if value_campo else value_campo
                        if not value_campo or value_campo == '':
                            value_campo = 'Vazio'
                        
                        if field_is_sigiloso(model,versao_inline.object_id,campo):
                            value_campo = '*** Esta observação/anotação é sigilosa ***'
                            
                        historico_inline.append({
                            'usuario': user.name,
                            'usuario_papel': str(user.papel),
                            'evento': tipo_events.get(event),
                            'tipo': model_name,
                            'verbose': mudancas.get('name'),
                            'campo': field.verbose_name,
                            'referencia': referencia or versao_inline.object_repr,
                            'valor': value_campo,
                            'criado_em': data_modificacao
                        })
                    except: pass
    
    return historico_inline

def field_is_sigiloso(model,id,field):
    fields_sigilosos = ['descricao','anotacao_defensor','anotacao','observacao','anotacao']
    field_sigilogo = hasattr(model,'sigiloso')
    field_anotacao_defensor_sigilosa = hasattr(model,'anotacao_defensor_sigilosa')
    if (field_sigilogo or field_anotacao_defensor_sigilosa) and field in fields_sigilosos:
        instance = model.objects.get(pk=id)
        if field_sigilogo:
            return instance and instance.sigiloso
        if field_anotacao_defensor_sigilosa:
            return instance and instance.anotacao_defensor_sigilosa
    return False