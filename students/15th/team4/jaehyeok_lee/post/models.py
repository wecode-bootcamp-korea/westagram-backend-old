from django.db import models
from django.utils import timezone

from user.models import User


class Post(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    img_url = models.CharField(max_length = 1000)
    content = models.TextField()
    datetime = models.DateTimeField(default = timezone.now)
    class Meta:
        db_table = 'posts'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    datetime = models.DateTimeField(default = timezone.now)
    class Meta:
        db_table = 'comments'
