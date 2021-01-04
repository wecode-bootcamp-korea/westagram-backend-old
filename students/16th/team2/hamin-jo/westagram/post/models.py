from django.db import models

from user.models import User

class Post(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post_time   = models.DateTimeField(auto_now_add=True, null=False)
    image       = models.URLField(max_length= 2000, null=False)

class Comment(models.Model):
    post         = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    user         = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    comment_time = models.DateTimeField(auto_now_add=True, null=False)
    comment      = models.TextField(max_length=50)