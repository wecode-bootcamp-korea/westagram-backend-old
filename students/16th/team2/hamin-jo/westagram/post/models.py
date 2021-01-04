import datetime

from django.db import models

from user.models import User

class Post(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post_time   = models.DateTimeField(auto_now_add=True, null=False)
    image       = models.URLField(max_length= 2000, null=False)