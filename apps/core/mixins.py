from django.conf import settings
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin import SimpleListFilter
from django.db import models
from django.forms import Select, Textarea, TextInput
from django.utils import timezone
import json
import decimal
import inspect

from django_currentuser.middleware import get_current_user
from reversion.admin import VersionAdmin
from reversion.revisions import is_active, set_comment
from django.contrib.admin.options import ModelAdmin as MA

LIST_PER_PAGE = 10


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

    class Meta:
        abstract = True

    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):
        if get_current_user():
            if (not self.criado_por or not self.criado_em) and get_current_user() and get_current_user().id:
                self.criado_por = get_current_user()
                self.criado_em = timezone.now()
            elif get_current_user() and get_current_user().id:
                self.modificado_por = get_current_user()
                self.modificado_em = timezone.now()
        super(BaseModel, self).save(force_insert=False,
                                    force_update=False,
                                    using=None,
                                    update_fields=None)


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

