from django.db import models

from account.models import User

class Post(models.Model):
    user       = models.ForeignKey(User, on_delete = models.CASCADE)
    text       = models.TextField()
    img_url    = models.URLField()
    created_at = models.DateTimeField(auto_now_add = True)

class Comment(models.Model):
    user       = models.ForeignKey(User, on_delete = models.CASCADE)
    post       = models.ForeignKey(Post, on_delete = models.CASCADE)
    text       = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)