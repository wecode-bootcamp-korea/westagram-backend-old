from django.db import models
from django.utils import timezone
from user.models import User

# Create your models here.


class BoardPosting(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    image    = models.CharField(max_length=1000, null=True)
    text     = models.TextField(max_length=100, null=True)
    time     = models.DateTimeField(default = timezone.now, null=True)

    class Meta:
        db_table = 'postings'

class BoardComment(models.Model):
    username = models.CharField(max_length=45)
    text     = models.TextField(max_length=100, null=True)
    itme     = models.DateTimeField(default = timezone.now, null=True)
    posting  = models.ForeignKey(BoardPosting, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'comments'
