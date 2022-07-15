from django.db import models
from accounts.models import User

class Todo(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200, unique=True)
    completed = models.BooleanField(default=False)
    user_id = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    us = user
    usid = us.split('@')[0]

    def __str__(self):
        return self.title