from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(default=timezone.now )
    notification_sent = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)  # Assuming task is linked to a user


    def __self__(self):
        return self.title
    

