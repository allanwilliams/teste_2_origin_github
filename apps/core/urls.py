from django.urls import path, include

app_name = "core"
urlpatterns = [
    path("api/", include("apps.core.api.urls")),
]
