from django.db import models


class Account(models.Model):
    email       = models.CharField(max_length=100)
    nickname    = models.CharField(max_length=20)
    name        = models.CharField(max_length=20)
    phonenumber = models.CharField(max_length=20)
    password    = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'accounts'

