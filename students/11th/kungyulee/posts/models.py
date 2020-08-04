from datetime import datetime 

from django.db import models

from accounts.models import User

class Post(models.Model):
    author     = models.ForeignKey(User, on_delete = models.CASCADE)
    contents   = models.TextField()
    image_url  = models.URLField(max_length = 200, blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.author)

class Comment(models.Model):
    author        = models.ForeignKey(User, on_delete = models.CASCADE)
    post          = models.ForeignKey(Post, on_delete = models.CASCADE)
    contents      = models.CharField(max_length = 300)
    created_at    = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'comment by {self.author}'
