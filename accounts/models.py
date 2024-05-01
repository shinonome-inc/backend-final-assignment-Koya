from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField()


class Friendship(models.Model):
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followings")
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)


class Meta:
    constraints = [
        models.UniqueConstraint(fields=["following", "follower"], name="follow_unique"),
    ]
