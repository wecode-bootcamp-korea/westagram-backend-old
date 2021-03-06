from django.conf.urls import url
from django.db import models

from user.models import User

class Post(models.Model):
    img_url     = models.URLField()
    create_date = models.DateTimeField(auto_now_add=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'posts'