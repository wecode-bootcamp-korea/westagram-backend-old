from django.db import models
from django.utils import timezone
from user.models import User


class Board(models.Model):
    board_name = models.CharField(max_length=45)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    image = models.CharField(max_length=200, blank=True)
    contents = models.TextField()

    class Meta:
        db_table = 'boards'


# Create your models here.
