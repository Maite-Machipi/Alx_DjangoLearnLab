from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer
from rest_framework import status

User = get_user_model()

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.get(user=user)

        return Response({
            "user": serializer.data,
            "token": token.key
        })

    return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key
        })

    return Response({"error": "Invalid credentials"}, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):

    user = request.user

    return Response({
        "username": user.username,
        "email": user.email,
        "bio": user.bio
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    if request.user.id == user_id:
        return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_to_follow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    request.user.following.add(user_to_follow)
    return Response({"detail": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    try:
        user_to_unfollow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    request.user.following.remove(user_to_unfollow)
    return Response({"detail": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)
