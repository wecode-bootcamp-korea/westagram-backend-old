from django.db import models
from django.utils import timezone

from user.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    image_url = models.URLField(max_length=500)

    class Meta:
        db_table = 'posts'
