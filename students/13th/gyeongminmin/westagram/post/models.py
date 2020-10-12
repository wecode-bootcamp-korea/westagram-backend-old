# autopep8: off
from django.db import models
from auth.models import Users

class Follows(models.Model):
    user_id     = models.ForeignKey(Users, related_name='user', on_delete=models.CASCADE)
    followed_by = models.ForeignKey(Users, related_name='followed_by', on_delete=models.CASCADE)

class Posts(models.Model):
    content = models.CharField(max_length=500)
    write_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

class PostLikes(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

class Comments(models.Model):
    content     = models.CharField(max_length=200)
    write_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    user     = models.ForeignKey(Users, on_delete=models.CASCADE)
    post    = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

class PostImage(models.Model):
    url = models.TextField()
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
