from rest_framework.routers import DefaultRouter
from apps.users.api.viewsets import (
    UserPreferenciasViewSet,
)

router = DefaultRouter()
router.register(r'user-preferencias', UserPreferenciasViewSet , basename='user_preferencias')
urlpatterns = router.urls
