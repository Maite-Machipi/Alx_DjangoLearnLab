from rest_framework import serializers
from .models import Workout, Meal, Goal

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ["id", "type", "duration_minutes", "calories_burned", "date", "created_at"]

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ["id", "name", "calories", "protein_g", "carbs_g", "fat_g", "date", "created_at"]

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ["id", "goal_type", "target_value", "start_date", "end_date", "created_at"]
