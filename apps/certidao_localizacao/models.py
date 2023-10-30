from statistics import mode
from django.db import models
from apps.core.mixins import BaseModel
from django.conf import settings
from apps.contrib.models import Estados

# Create your models here.
class Certidao(BaseModel):
    ip = models.CharField(max_length=20,null=True,blank=True)
    municipio = models.CharField(max_length=500,null=True,blank=True)
    data_hora = models.DateTimeField(blank=True, null=True)
    assinatura = models.BooleanField(blank=True, null=True,default=False)
    latitude = models.CharField(blank=True, null=True, max_length=50)
    longitude = models.CharField(blank=True, null=True, max_length=50)
    estado = models.ForeignKey(
        Estados,
        verbose_name=("Estado"),
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True
    )

    crypted_fields = ['municipio',]

    class Meta:
        verbose_name = 'Certidão'
        verbose_name_plural = 'Certidões'
        
class CertidaoAssinatura(BaseModel):
    token = models.CharField('Token validador', null=True, blank=True, max_length=16)
    certidao = models.ForeignKey(Certidao,
                                verbose_name='Certidao',
                                on_delete=models.DO_NOTHING,
                                null=True, blank=True)
    def __str__(self):
        return self.token
    class Meta:
        verbose_name = 'Certidão Assinatura'
        verbose_name_plural = 'Certidões Assinatura'