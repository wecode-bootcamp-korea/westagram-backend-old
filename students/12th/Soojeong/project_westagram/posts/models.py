from django.db import models
from user.models import Users
from django.utils import timezone

class Posts(models.Model):
    user        = models.ForeignKey(Users, on_delete = models.CASCADE)
    pub_date    = models.DateTimeField(auto_now_add=True)
    image_url   = models.URLField()
    pub_content = models.CharField(max_length=500, null=True)
