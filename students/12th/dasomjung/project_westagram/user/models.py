from django.db import models


class Users(models.Model):
    name             = models.CharField(max_length=50)
    user_name        = models.CharField(max_length=50)
    phone_number     = models.IntegerField(default=0)
    email            = models.CharField(max_length=50)
    password         = models.CharField(max_length=300)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)
