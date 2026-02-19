from django.urls import path
from . import views

urlpatterns = [
    # User Registration
    path("register/", views.register, name="register"),

    # User Login
    path("login/", views.login_view, name="login"),

    # User Profile (optional but recommended)
    path("profile/", views.profile, name="profile"),
]
