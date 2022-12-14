from django.db import models

from Test.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    path = models.CharField(blank=False, max_length=1000)
    content = models.TextField()
    modified_date = models.DateTimeField(auto_now_add=True)


class LikesComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    is_liked = models.BooleanField(null=True)



