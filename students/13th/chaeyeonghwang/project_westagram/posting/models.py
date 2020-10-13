from django.db import models
from django.utils import timezone

# Create your models here.
class Posting(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now=True)
    img = models.ImageField(upload_to=None, height_field=None, width_field=None)
    description = models.TextField(null=True)

    class Meta():
        db_table = 'postings'

class Comment(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post = models.OneToOneField(Posting, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta():
        db_table = 'comments'


class Reply(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now=True)
    content = models.TextField()

    class Meta():
        db_table = 'replies' 

class Like(models.Model):
    post = models.ForeignKey(Posting, on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta():
        db_table = 'likes'
