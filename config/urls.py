from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView
from django.views.generic.base import RedirectView
from ajax_select import urls as ajax_select_urls

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('django_sso_app/', include('apps.django_sso_app.urls')),
    path('core/', include('apps.core.urls')),
    path('oidc/', include('mozilla_django_oidc.urls')),
    path("users/", include("apps.users.urls", namespace="users")),
    path('ajax_select/', include(ajax_select_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.USE_FUSIONAUTH:
    urlpatterns += [
        path('', RedirectView.as_view(url=reverse_lazy('sso_login'))),
        path('admin/login/',RedirectView.as_view(url=reverse_lazy('sso_login'))),
    ]
else:
    urlpatterns += [ path('', RedirectView.as_view(url=reverse_lazy('admin:index'))) ]

urlpatterns += [path('admin/', admin.site.urls),]

