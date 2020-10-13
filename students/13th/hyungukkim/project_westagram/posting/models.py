from django.db import models
from user.models import Account

class Post(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    contents = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    img_url = models.CharField(max_length=200)
    likes_count = models.IntegerField(default=0)

class Comment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    contents = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)

class Likes(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class ByComment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    contents = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)