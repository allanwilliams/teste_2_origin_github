from rest_framework.serializers import ModelSerializer
from apps.users.models import UserPreferencias

class UserPreferenciasSerializer(ModelSerializer):
    class Meta:
        model = UserPreferencias
        fields = '__all__'
        