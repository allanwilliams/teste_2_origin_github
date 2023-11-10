from rest_framework.viewsets import ModelViewSet
from apps.users.models import UserPreferencias
from .serializers import UserPreferenciasSerializer
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination

class ResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserPreferenciasFilter(filters.FilterSet):
    class Meta:
        model = UserPreferencias
        fields = {
            'user': ['exact'],
        }

class UserPreferenciasViewSet(ModelViewSet):
    queryset = UserPreferencias.objects.all()
    serializer_class = UserPreferenciasSerializer
    filterset_class = UserPreferenciasFilter
    http_method_names = ['get', 'patch', 'post', 'delete']
