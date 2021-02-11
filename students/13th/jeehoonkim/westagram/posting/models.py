from django.db import models

from user.models import User

class Posting(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user_posting')
    content       = models.TextField(null = True)
    image         = models.URLField()
    created_date  = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True, null = True)
    like          = models.ManyToManyField(User, related_name = 'like_posting', through = 'PostingLike')

    class Meta: 
        db_table = 'postings'

class PostingLike(models.Model):
    posting = models.ForeignKey(Posting, related_name='posting_like', on_delete=models.CASCADE)
    user    = models.ForeignKey(User, related_name='user_like', on_delete=models.CASCADE)

    class Meta: 
        db_table = 'postings_likes'


class Comment(models.Model):
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    posting       = models.ForeignKey(Posting, on_delete=models.CASCADE)
    content       = models.CharField(max_length=2000)
    created_date  = models.DateTimeField()
    modified_date = models.DateTimeField(null=True)
    thread_to     = models.IntegerField(null=True, blank=True)

    class Meta: 
        db_table = 'comments'