from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    daily_points = models.IntegerField(default=10)

    def __str__(self):
        return str(self.user.username)
