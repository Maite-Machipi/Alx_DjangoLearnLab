from django.urls import path
from .views import UserListView, FollowUserView, UnfollowUserView

urlpatterns = [
    # User Registration
    path("register/", views.register, name="register"),

    # User Login
    path("login/", views.login_view, name="login"),

    # User Profile (optional but recommended)
    path("profile/", views.profile, name="profile"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("follow/<int:user_id>/", views.follow_user, name="follow-user"),
    path("unfollow/<int:user_id>/", views.unfollow_user, name="unfollow-user"),
]
