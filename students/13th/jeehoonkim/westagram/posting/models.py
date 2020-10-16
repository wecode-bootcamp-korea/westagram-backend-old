from django.db import models

from user.models import User

class Posting(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user_posting')
    content       = models.TextField(null = True)
    image         = models.URLField()
    created_date  = models.DateTimeField()
    modified_date = models.DateTimeField(null = True)
    like          = models.ManyToManyField(User, related_name = 'like_posting')

    class Meta: 
        db_table = 'postings'

class Comment(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    posting       = models.ForeignKey(Posting, on_delete=models.CASCADE)
    content       = models.CharField(max_length=2000)
    created_date  = models.DateTimeField()
    modified_date = models.DateTimeField(null=True)
    thread_to     = models.IntegerField(null=True, blank=True)

    class Meta: 
        db_table = 'comments'