from operator import mod
from pyexpat import model
from statistics import mode
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_posts")
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User, related_name="liked_post", blank=True)
  
    def serialize(self):
        return {
            "id": self.id,
            "creator": self.creator.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.users.count(),
            "user": [user.username for user in self.users.all()],
        }


class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers_user")
    follower = models.ManyToManyField(User, blank=True, related_name="following")


class Comments(models.Model):
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="comments_post")
