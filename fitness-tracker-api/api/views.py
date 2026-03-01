from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from datetime import timedelta

from .models import Activity
from .serializers import ActivitySerializer


class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return the logged-in user's activities
        queryset = Activity.objects.filter(user=self.request.user).order_by("-date")

        # Optional filters (for polish/demo)
        activity_type = self.request.query_params.get("activity_type")
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type.upper())

        days = self.request.query_params.get("days")
        if days and days.isdigit():
            queryset = queryset.filter(date__gte=now() - timedelta(days=int(days)))

        return queryset

    def perform_create(self, serializer):
        # Automatically attach the logged in user
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def history(self, request):
        # Same as list, but explicit endpoint for the requirement
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def summary(self, request):
        queryset = self.get_queryset()

        total_activities = queryset.count()
        total_minutes = sum(a.duration for a in queryset)
        total_calories = sum(a.calories_burned for a in queryset)

        return Response({
            "total_activities": total_activities,
            "total_minutes": total_minutes,
            "total_calories": total_calories,
        })
