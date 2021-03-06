from django.db import models
from user.models import User

class Post(models.Model):
    user       = models.ForeignKey("user.User", on_delete=models.CASCADE)
    image_url  = models.CharField(max_length=3000, null=False)
    content    = models.CharField(max_length=2000, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "posts"