from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Workout, Meal, Goal
from .serializers import WorkoutSerializer, MealSerializer, GoalSerializer
from datetime import date
from django.utils.dateparse import parse_date
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.db.models import Sum

class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user).order_by("-date", "-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MealViewSet(viewsets.ModelViewSet):
    serializer_class = MealSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user).order_by("-date", "-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="progress")
    def progress(self, request):
        goals = self.get_queryset()
        results = []

        for goal in goals:
            start = goal.start_date
            end = goal.end_date

            workouts = Workout.objects.filter(user=request.user, date__range=[start, end])
            meals = Meal.objects.filter(user=request.user, date__range=[start, end])

            progress_value = 0

            if goal.goal_type == "minutes":
                progress_value = workouts.aggregate(total=Sum("duration_minutes"))["total"] or 0
            elif goal.goal_type == "workouts":
                progress_value = workouts.count()
            elif goal.goal_type == "calories":
                progress_value = workouts.aggregate(total=Sum("calories_burned"))["total"] or 0
            elif goal.goal_type == "steps":
                progress_value = 0
            elif goal.goal_type == "water":
                progress_value = 0

            target = goal.target_value
            percent = round((progress_value / target) * 100, 2) if target else 0

            results.append({
                "goal_id": goal.id,
                "goal_type": goal.goal_type,
                "target_value": target,
                "date_range": {"start": start.isoformat(), "end": end.isoformat()},
                "progress_value": progress_value,
                "percent_complete": min(percent, 100.0),
                "is_completed": (progress_value >= target) if target else False,
            })

        return Response({"count": len(results), "goals": results})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def daily_summary(request):
    # /api/v1/summary/?date=2026-03-01
    d = parse_date(request.query_params.get("date") or "") or date.today()

    workouts = Workout.objects.filter(user=request.user, date=d)
    meals = Meal.objects.filter(user=request.user, date=d)

    workout_minutes = workouts.aggregate(total=Sum("duration_minutes"))["total"] or 0
    calories_burned = workouts.aggregate(total=Sum("calories_burned"))["total"] or 0
    calories_eaten = meals.aggregate(total=Sum("calories"))["total"] or 0

    return Response({
        "date": d.isoformat(),
        "workouts_count": workouts.count(),
        "workout_minutes": workout_minutes,
        "calories_burned": calories_burned,
        "meals_count": meals.count(),
        "calories_eaten": calories_eaten,
        "net_calories": calories_eaten - calories_burned,
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def stats(request):
    # /api/v1/stats/?start=2026-03-01&end=2026-03-07
    start = parse_date(request.query_params.get("start") or "") or date.today()
    end = parse_date(request.query_params.get("end") or "") or date.today()

    workouts = Workout.objects.filter(user=request.user, date__range=[start, end])
    meals = Meal.objects.filter(user=request.user, date__range=[start, end])

    workout_minutes = workouts.aggregate(total=Sum("duration_minutes"))["total"] or 0
    calories_burned = workouts.aggregate(total=Sum("calories_burned"))["total"] or 0
    calories_eaten = meals.aggregate(total=Sum("calories"))["total"] or 0

    return Response({
        "range": {"start": start.isoformat(), "end": end.isoformat()},
        "workouts_count": workouts.count(),
        "workout_minutes": workout_minutes,
        "calories_burned": calories_burned,
        "meals_count": meals.count(),
        "calories_eaten": calories_eaten,
        "net_calories": calories_eaten - calories_burned,
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def goals_progress(request):
    goals = Goal.objects.filter(user=request.user).order_by("-created_at")

    results = []

    for goal in goals:
        start = goal.start_date
        end = goal.end_date

        workouts = Workout.objects.filter(user=request.user, date__range=[start, end])
        meals = Meal.objects.filter(user=request.user, date__range=[start, end])

        progress_value = 0

        if goal.goal_type == "minutes":
            progress_value = workouts.aggregate(total=Sum("duration_minutes"))["total"] or 0

        elif goal.goal_type == "workouts":
            progress_value = workouts.count()

        elif goal.goal_type == "calories":
            # Here we interpret "calories" goal as calories burned (from workouts)
            progress_value = workouts.aggregate(total=Sum("calories_burned"))["total"] or 0

        elif goal.goal_type == "steps":
            # Not implemented yet (we don't have steps model)
            progress_value = 0

        elif goal.goal_type == "water":
            # Not implemented yet (we don't have water intake model)
            progress_value = 0

        target = goal.target_value
        percent = round((progress_value / target) * 100, 2) if target else 0

        results.append({
            "goal_id": goal.id,
            "goal_type": goal.goal_type,
            "target_value": target,
            "date_range": {"start": start.isoformat(), "end": end.isoformat()},
            "progress_value": progress_value,
            "percent_complete": min(percent, 100.0),
            "is_completed": progress_value >= target if target else False,
        })

    return Response({
        "count": len(results),
        "goals": results
    })
