from django.db import models
from Account.models import Account

class Posting(models.Model):

     user      = models.ForeignKey(Account, on_delete=models.CASCADE)
     time      = models.TimeField(auto_now_add=True)
     image_url = models.URLField(max_length=100)
     contents  = models.CharField(max_length=100)