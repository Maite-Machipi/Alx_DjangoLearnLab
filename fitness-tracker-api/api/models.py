from django.db import models
from django.contrib.auth.models import User


class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('RUNNING', 'Running'),
        ('WALKING', 'Walking'),
        ('CYCLING', 'Cycling'),
        ('GYM', 'Gym'),
        ('SWIMMING', 'Swimming'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    duration = models.IntegerField(help_text="Duration in minutes")
    calories_burned = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"
