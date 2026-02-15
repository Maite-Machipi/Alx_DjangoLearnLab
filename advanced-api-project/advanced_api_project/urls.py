from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # This connects your api app URLs
    path('api/', include('api.urls')),
]
