from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("admin/", admin.site.urls),

    # Version 1 (new clean API)
    path("api/v1/", include("api.urls")),

    # Token endpoint
    path("api/v1/auth/token/", obtain_auth_token),

    # Browser login (optional but helpful)
    path("api-auth/", include("rest_framework.urls")),
]
