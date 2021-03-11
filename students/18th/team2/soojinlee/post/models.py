import datetime

from django.utils import timezone
from django.db   import models

from datetime import timedelta
from user.models import User


class Post(models.Model):
    image       = models.URLField(max_length=500)
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posts'