
from django.db import models

class Post(models.Model):
    image_url = models.CharField(max_length=3000)
    contents  = models.CharField(max_length=1000)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    account   = models.ForeignKey('users.Account', on_delete=models.CASCADE)

    class Meta:
        db_table = 'postings'


class Comment(models.Model):
    comments  = models.CharField(max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    posting   = models.ForeignKey('Post', on_delete=models.CASCADE)
    account   = models.ForeignKey('users.Account', on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments'

class Like(models.Model):
    like_at   = models.DateTimeField(auto_now_add=True)
    posting   = models.ForeignKey('Post', on_delete=models.CASCADE)
    account   = models.ForeignKey('users.Account', on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'
