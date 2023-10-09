from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save, pre_save
from django.conf import settings
from django_currentuser.middleware import get_current_authenticated_user
from apps.users.choices import  CHOICES_SEXO_USER
from apps.core.mixins import BaseModel
from django.utils import timezone

class User(AbstractUser):
    PAPEL_DEFENSOR = 1
    
    cols = {
        'name': 3,
        'papel':3,
        'matricula':3,
        'num_orgao_classe':3,
        'username':4,
        'email': 4,
        'password':4,
        'cpf': 3,
        'first_name': 3,
        'last_name': 3
    }
  
    name = CharField(_("Nome Completo"), blank=True, max_length=255)
    papel = models.ForeignKey(
        'users.Papeis',
        verbose_name='Papeis',
        on_delete=models.PROTECT,
        related_name='%(class)s_papel',
        null=True,
        db_index=True,
    )
    matricula = models.CharField(
        'Matricula',
        max_length=11,
        help_text="Obrigatório para cadastro de defensores",
        unique=True,
        blank=True,
        null=True)
    num_orgao_classe = CharField(_("Número do Órgão de Classe"),
                                 blank=True,
                                 null=True,
                                 max_length=255)

    cpf = models.CharField('CPF', max_length=14, unique=True, null=True, blank=True)

   
    sexo = models.IntegerField(_("Sexo"), choices=CHOICES_SEXO_USER,
                               default=0,)
    user_str = models.CharField('User String',
                                blank=True, null=True, max_length=200)
  
		    
    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):
        if self.name:
            if ' ' in self.name:
                name = self.name.split(' ')
            else:
                name = [self.name, self.name]
            if not self.first_name:
                self.first_name = name[0]
            if not self.last_name:
                self.last_name = name[-1]
        
        if self.id:
            if self.first_name:
                self.user_str = '{:08n} {} {} ({})'.format(self.id, self.first_name, self.last_name,self.username)
        
        super(User, self).save(
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
        )

    def __str__(self):
        return '{:08n} {} {} ({})'.format(self.id, self.first_name or '', self.last_name or '', self.username)


    def is_defensor(self):
        if self.papel_id in (self.PAPEL_DEFENSOR,):
            return True
        else:
            return False
    
    def get_user_preferencias(self):
        preferencias_obj = {}
        if self:
            preferencias = UserPreferencias.objects.filter(user=self)
            tipos = UserPreferencias.Tipos
            

            for tipo in tipos:
                preferencias_obj[tipo.name] = {
                    'id': tipo.value,
                    'label':tipo.label,
                    'value':preferencias.filter(preferencia=tipo).first() or False
                }
        return preferencias_obj
    

@receiver(post_save, sender=User)
def create_app_user_str(sender, instance, created, **kwargs):
    if created:
        if instance.name:
            if ' ' in instance.name:
                name = instance.name.split(' ')
            else:
                name = [instance.name, instance.name]

        instance.user_str = '{:08n} {} {} ({})'.format(instance.id, instance.first_name, instance.last_name,instance.username)
        instance.save() 


class Papeis(BaseModel):
    titulo = models.CharField(
        'Título',
        max_length=25,
    )

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Papel'
        verbose_name_plural = 'Papeis'
        ordering = [
            'titulo',
        ]


class Defensores(BaseModel):
    nome = models.CharField('Nome', max_length=150)
    matricula = models.CharField('Matricula', max_length=11)
    cpf = models.CharField('CPF', max_length=11)
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_usuario',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Defensores'
        verbose_name_plural = 'Defensores'
        ordering = ['nome', ]


class DefensoresLotacoes(BaseModel):
    cols = {
        'defensor': 3,
        'especie': 2,
        'data_inicio': 2,
        'data_termino': 2,
        'defensor_matricula': 2,
        'local_atuacao': 4,
        'defensor_cpf': 2,
        'defensor_email': 2,
        'user': 2,
        'nucleo': 2,
        'defensoria': 4,
        'tipo': 2,
        'ativo': 1,
        'origem_id': 2,
        'origem': 4,
        'titularidade_designacao': 2,
        'defensoreslocacoes_str': 4,
        'criado_por': 4,
        'criado_em': 2,
        'modificado_por': 4,
        'modificado_em': 2
    }

    defensor_nome = models.CharField('Defensor', max_length=255)
    defensor_matricula = models.CharField('Matricula', max_length=11, db_index=True)
    defensor_cpf = models.CharField('CPF', max_length=11)
    defensor_email = models.CharField('E-mail', max_length=255, null=True)
    defensoria = models.CharField('Defensoria', max_length=255)
    tipo = models.CharField('Tipo', max_length=50)
    titularidade_designacao = models.CharField('Titularidade ou Designação',
                                               max_length=50)
    origem = models.CharField('Origem', max_length=255)
    origem_id = models.IntegerField('Identificador da Origem')
    data_inicio = models.DateField(
        'Data de Início',
        db_index=True,)
    data_termino = models.DateField(
        'Data de Término',
        null=True,
        blank=True,
        db_index=True,
    )
    nucleo_txt = models.CharField(
        'Núcleo',
        max_length=255,
        null=True,
        blank=True,
    )
    # nucleo = models.ForeignKey(
    #     'contrib.Nucleos',
    #     verbose_name='Núcleo',
    #     on_delete=models.DO_NOTHING,
    #     related_name='%(class)s_nucleo',
    #     null=True,
    #     blank=True,
    # )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_usuario',
        null=True,
        blank=True,
        db_index=True,
    )
    defensor = models.ForeignKey(
        Defensores, on_delete=models.PROTECT,
        related_name='%(class)s_defensores',
        verbose_name='Defensor',
        null=True, blank=True,
        db_index=True,)
    defensoreslocacoes_str = models.CharField(
        'Defensor(a)/Defensoria',
        max_length=255,
        null=True,
        blank=True,
    )
    ativo = models.BooleanField('Está ativa?', blank=True, default=True)

    def __str__(self):
       return '{} - {}'.format(self.defensor_nome, self.defensoria)

    def save(self, *args, **kwargs):
        from datetime import datetime
        from django.db.models import Q
        DefensoresLotacoes.objects. \
            exclude(data_inicio__lte=datetime.now()). \
            exclude(Q(data_termino__gte=datetime.now()) | Q(data_termino__isnull=True)). \
            update(ativo=False)
        self.defensoreslocacoes_str = '{} - {}'.format(self.defensor_nome, self.defensoria)
        super(DefensoresLotacoes, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Lotação dos defensores'
        verbose_name_plural = 'Lotações dos defensores'
        ordering = ['-data_inicio', ]

class UserPreferencias(BaseModel):

    class Tipos(models.IntegerChoices):
        MENU_COMPACTO = 1, 'Habilitar menu compacto'
    
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='%(class)s_user',
    )

    preferencia = models.IntegerField('Preferência', choices=Tipos.choices)

    class Meta:
        verbose_name = 'Preferência do Usuário'
        verbose_name_plural = 'Preferências dos Usuários'

class TrocaSenhaUsuario(BaseModel):
    user = models.ForeignKey(
        'User',
        on_delete=models.DO_NOTHING,
        related_name='%(class)s_usuario',
        null=True,
        blank=True,
        db_index=True,
    )
    
    password = models.CharField(_('password'), max_length=128)
    
    @receiver(pre_save, sender=User)
    def user_updated(sender, **kwargs):
        if not settings.USE_FUSIONAUTH:
            try:
                user = kwargs.get('instance', None)
                if user and hasattr(user,'pk'):
                        user_old = User.objects.get(pk=user.pk)
                        if user and user_old:
                            if user.password != user_old.password:
                                dict_password = {
                                    'user': user,
                                    'password': user.password,
                                    'criado_em': timezone.now()
                                }
                                grava_senha = TrocaSenhaUsuario(**dict_password)
                                grava_senha.save()
            except:
                pass