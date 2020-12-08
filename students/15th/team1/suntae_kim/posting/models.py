from django.db import models
from django.utils import timezone
from user.models import User

# Create your models here.


class BoardPosting(models.Model):
    posting_username = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    posting_image    = models.CharField(max_length=1000, null=True)
    posting_text     = models.TextField(max_length=100, null=True)
    posting_time     = models.DateTimeField(default = timezone.now, null=True)

    class Meta:
        db_table = 'postings'

class BoardComment(models.Model):
    comment_username = models.CharField(max_length=45, null=True)
    comment_text     = models.TextField(max_length=100, null=True)
    comment_itme     = models.DateTimeField(default = timezone.now, null=True)
    posting          = models.ForeignKey(BoardPosting, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'comments'
