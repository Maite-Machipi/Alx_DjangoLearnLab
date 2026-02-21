from django.urls import path
from .views import register, UserListView, FollowUserView, UnfollowUserView

urlpatterns = [
    path("register/", register, name="register"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("follow/<int:user_id>/", FollowUserView.as_view(), name="follow-user"),
    path("unfollow/<int:user_id>/", UnfollowUserView.as_view(), name="unfollow-user"),
]
