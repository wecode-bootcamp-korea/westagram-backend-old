from django.db import models

from User.models import User

class Post(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    img_url    = models.URLField()
    content    = models.TextField()
