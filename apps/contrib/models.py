from django.db import models

from apps.core.mixins import BaseModel
from django.utils.translation import gettext_lazy as _

class Estados(BaseModel):
    nome = models.CharField('Nome', max_length=20)
    sigla = models.CharField('Sigla', max_length=2)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
