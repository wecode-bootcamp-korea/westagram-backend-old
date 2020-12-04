from django.db import models
from django.utils import timezone

from user.models import User

# Create your models here.


class Board(models.Model):
#    user = models.ForeignKey('User', on_delete=models.CASCADE)
#    submit_time = models.DateTimeField(default = timezone.now, null=True)
    username = models.CharField(max_length=45, null=True)
    image_url = models.CharField(max_length=1000, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'boards'

