from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityViewSet, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"activities", ActivityViewSet, basename="activities")

urlpatterns = [
    path("", include(router.urls)),
]
