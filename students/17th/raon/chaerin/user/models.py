from django.db import models

# Create your models here.

class Account(models.Model):
    username  = models.CharField(max_length=20, null=True)
    email     = models.CharField(max_length=200, unique=True)
    password  = models.CharField(max_length=250)
    phone_num = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = 'accounts'

