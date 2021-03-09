from django.conf.urls import url
from django.db import models

from user.models import User

class Post(models.Model):
    content     = models.TextField()
    img_url     = models.URLField()
    create_date = models.DateTimeField(auto_now_add=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'posts'

class Comment(models.Model):
    post        = models.ForeignKey('Post', on_delete=models.CASCADE)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    content     = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = 'comments'