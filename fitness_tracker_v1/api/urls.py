from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkoutViewSet, MealViewSet, GoalViewSet, daily_summary, stats, goals_progress

router = DefaultRouter()
router.register("workouts", WorkoutViewSet, basename="workouts")
router.register("meals", MealViewSet, basename="meals")
router.register("goals", GoalViewSet, basename="goals")


urlpatterns = [
    path("", include(router.urls)),
    path("summary/", daily_summary),
    path("stats/", stats),
    path("goals/progress/", goals_progress),
]
