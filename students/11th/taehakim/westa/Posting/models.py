from django.db import models
from Account.models import Account

class Posting(models.Model):

     user      = models.ForeignKey(Account, on_delete=models.CASCADE)
     time      = models.TimeField(auto_now_add=True)
     image_url = models.URLField(max_length=100)
     contents  = models.CharField(max_length=100)


class Comment(models.Model):

     user_name    = models.ForeignKey(Account, on_delete=models.CASCADE)
     writing_time = models.TimeField(auto_now=True)
     comment      = models.CharField(max_length=300)
     post         = models.ForeignKey(Posting, on_delete=models.CASCADE)

