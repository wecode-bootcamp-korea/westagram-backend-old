from django.db import models
from user.models import User

class Post(models.Model):
    user          = models.ForeignKey(User,on_delete=models.CASCADE)
    created_time  = models.DateTimeField(auto_now_add=True)
    image_url     = models.URLField(null=True)
    content       = models.TextField(max_length=1000,null=True)

    class Meta:
        db_table='posts'

class Comment(models.Model):
    user          = models.ForeignKey(User,on_delete=models.CASCADE)
    post          = models.ForeignKey(Post,on_delete=models.CASCADE)
    created_time  = models.DateTimeField(auto_now_add=True)
    comment       = models.TextField(max_length=100)

    class Meta:
        db_table='comments'
