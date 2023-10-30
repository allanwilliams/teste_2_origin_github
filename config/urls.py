from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django_currentuser.middleware import get_current_authenticated_user
from django.http import FileResponse, Http404
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView
from ajax_select import urls as ajax_select_urls
from apps.core.pastas_bloquedas import pastas_bloqueadas,arr_media_year_month
from apps.core.encrypt_url_utils import decrypt
import os

@login_required
def secure_file(request,nome_arquivo,year = None,month=None):
    #raise Http404
    access = False
    split_meta = str(request.META['PATH_INFO']).split('/')
    # file = split_meta.pop()
    # print(file)
    # split_meta = '/'.join(split_meta)
    for pasta in pastas_bloqueadas.keys():        
        if pasta == split_meta[2]:
            for accesses in pastas_bloqueadas[pasta]:
                if accesses == 'all':
                    access = True
                    break                    
                if request.user.has_perm(accesses):
                    access = True
                    break

        if split_meta[2] == 'estagio':
                access = True
                break
           
    if access:
        if(get_current_authenticated_user()):
            if year is None and month is None:
                path = request.path.split("/media/")[1].split('/')
                arquivo = path.pop()
                path = '/'.join(path)

            else:
                path = request.path.split("/media/")[1].split('/')
                arquivo = path.pop()
                path = '/'.join(path)

            arquivo = decrypt(arquivo)
            file_path = os.path.join(settings.MEDIA_ROOT, f'{path}/{arquivo}')
            if os.path.exists(file_path):
                return FileResponse(open(file_path,'rb'))
            raise Http404
        else:
            raise Http404
    else:
        raise Http404     
    
urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('django_sso_app/', include('apps.django_sso_app.urls')),
    path('core/', include('apps.core.urls')),
    path('oidc/', include('mozilla_django_oidc.urls')),
    path("users/", include("apps.users.urls", namespace="users")),
    path("certidao_localizacao/", include("apps.certidao_localizacao.urls", namespace="certidao_localizacao")),
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

