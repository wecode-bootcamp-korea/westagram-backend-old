from django.db import models

from user.models import User

class Post(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url  = models.URLField(max_length=2000)
    content    = models.TextField(null=True)

    class Meta:
        db_table = 'posts'
