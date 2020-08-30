from django.db   import models
from user.models import User

class Post(models.Model):
    user       = models.ForeignKey(User, on_delete = models.CASCADE)
    content    = models.TextField(max_length = 300)
    image_url  = models.URLField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now     = True)

class Comment(models.Model):
    post       = models.ForeignKey(Post, on_delete = models.CASCADE, null = True, blank = True)
    user       = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = 400)
    email      = models.CharField(max_length = 50)
    content    = models.CharField(max_length = 500)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now     = True)