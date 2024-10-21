from rest_framework.serializers import ModelSerializer
from apps.lembrete.models import Lembretes
from rest_framework import serializers
from apps.core.encrypt_url_utils import encrypt

class LembretesSerializer(ModelSerializer): # pragma: no cover
    documento = serializers.SerializerMethodField('get_documento')
    encid = serializers.SerializerMethodField('get_encid')
    class Meta:
        model = Lembretes
        fields = '__all__'

    def get_documento(self,obj):
        if obj.documento:
            diretorio,nome = str(obj.documento).split('/')
            return str(f"/media/{diretorio}/{encrypt(nome)}")
        
    def get_encid(self,obj):
        if obj:
            return obj.get_encrypt_id()