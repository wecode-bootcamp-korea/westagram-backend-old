from django.db import models

from user.models import User

class Posting(models.Model):
    image        = models.TextField(max_length=1000)
    caption      = models.TextField(max_length=1000, null=True)
    posted_time  = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True) 
    user         = models.ForeignKey('user.user', on_delete=models.CASCADE)

    class Meta:
        db_table = 'postings'

class Comment(models.Model):
    text         = models.CharField(max_length=200)
    posted_time  = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True) 
    posting      = models.ForeignKey('Posting', on_delete=models.CASCADE)
    user         = models.ForeignKey('user.user', on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments'
