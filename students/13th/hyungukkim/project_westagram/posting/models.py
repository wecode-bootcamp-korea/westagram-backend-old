from django.db import models
from user.models import Account

class Post(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    contents = models.CharField(max_length=200)
    create_time = models.DateTimeField(auto_now_add=True)
    img_url = models.CharField(max_length=200)
