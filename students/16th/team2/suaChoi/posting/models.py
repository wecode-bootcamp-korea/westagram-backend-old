from django.db import models

from user.models import User

class Post(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url    = models.URLField(max_length=2000)
    content      = models.TextField(null=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "posts"

class Comment(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    reply      = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comments"