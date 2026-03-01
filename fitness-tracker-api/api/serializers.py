from rest_framework import serializers
from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ["id", "user", "activity_type", "duration", "calories_burned", "date"]
        read_only_fields = ["id", "user", "date"]
