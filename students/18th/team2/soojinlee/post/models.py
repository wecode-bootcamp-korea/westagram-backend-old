import datetime
from datetime    import timedelta

from django.utils import timezone
from django.db    import models

from user.models import User


class Post(models.Model):
    image       = models.URLField(max_length=500)
    user        = models.ForeignKey(User,on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500)

    class Meta:
        db_table = 'posts'