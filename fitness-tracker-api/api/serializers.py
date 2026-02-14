from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Activity


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = ["id", "user", "activity_type", "duration", "calories_burned", "date"]
