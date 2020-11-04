from django.db import models
from user.models import User
# Create your models here.

class Post(models.Model):
    userName = models.ForeignKey(User, on_delete = models.CASCADE, null = False)
    pubTime = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length = 1000)
    imageUrl = models.URLField(max_length = 200)
   