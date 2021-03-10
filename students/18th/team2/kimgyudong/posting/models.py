from django.db import models

from user.models import User

class Post(models.Model):
    time = models.DateTimeField()
    content = models.CharField(max_length=500)
    image_url = models.URLField(max_length=200)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
