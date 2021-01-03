from django.db import models

from user.models import User

class Post(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post_time   = models.DateTimeField(null=False)
    image       = models.URLField(max_length= 2000, null=False)