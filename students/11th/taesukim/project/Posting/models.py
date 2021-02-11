from django.db import models

from User.models import User

class Post(models.Model):
    user       = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'user_id')
    created_at = models.DateTimeField(auto_now_add = True)
    img_url    = models.URLField()
    content    = models.TextField(null = True)
    liked_user = models.ManyToManyField(User, related_name = 'liked_user')

class Comment(models.Model):
    user       = models.ForeignKey(User, on_delete = models.CASCADE)
    post       = models.ForeignKey(Post, on_delete = models.CASCADE)
    comment    = models.TextField(null = True)
    created_at = models.DateTimeField(auto_now_add = True)

