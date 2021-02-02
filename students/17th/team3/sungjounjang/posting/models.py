from django.db import models

from user.models import Accounts

class Posting(models.Model):
    account   = models.ForeignKey('user.accounts', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=3000)
    contents  = models.CharField(max_length=300)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posting'
