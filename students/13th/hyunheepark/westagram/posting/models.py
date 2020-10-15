from django.db import models
from user.models import User 

# Create your models here.

class Post(models.Model):
    user       = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    img_url    = models.CharField(max_length=245)
    content    = models.TextField()
    like       = models.IntegerField(default=0)

    class Meta:
        db_table = 'posts'

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey('Post',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment_content = models.TextField()

    class Meta:
        db_table = 'comments'
    
