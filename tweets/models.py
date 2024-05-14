from django.conf import settings
from django.db import models


class Tweet(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    content = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.content} ({self.created_at})"


class Like(models.Model):
    likeuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liketweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="like_tweet")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["likeuser", "liketweet"], name="unique_like")]
