from django.db import models

from user.models import User

class Post(models.Model):
    image        = models.CharField(max_length=1000)
    caption      = models.CharField(max_length=1000, null=True)
    posted_time  = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    user         = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'posts'

class Comment(models.Model):
    text         = models.CharField(max_length=200)
    posted_time  = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True) 
    post         = models.ForeignKey('Post', on_delete=models.CASCADE)
    user         = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments'

class Like(models.Model):
    user            = models.ForeignKey('user.User', on_delete=models.CASCADE)
    post            = models.ForeignKey('Post', on_delete=models.CASCADE)
    liked_time      = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'likes'
