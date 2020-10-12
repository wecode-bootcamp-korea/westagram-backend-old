# autopep8: off
from django.db   import models
from auth.models import Users

class Follows(models.Model):
    user_id     = models.ForeignKey(Users, related_name='user', on_delete=models.CASCADE)
    followed_by = models.ForeignKey(Users, related_name='followed_by', on_delete=models.CASCADE)

class Posts(models.Model):
    content = models.CharField(max_length=500)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

class PostLikes(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)

class Comments(models.Model):
    content     = models.CharField(max_length=200)
    write_time  = models.DateField(auto_now=False, auto_now_add=False)
    update_time = models.DateField(auto_now=False, auto_now_add=False)
    user_id     = models.ForeignKey(Users, on_delete=models.CASCADE)
    post_id     = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment_id  = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

class PostImage(models.Model):
    url = models.TextField()
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE)
