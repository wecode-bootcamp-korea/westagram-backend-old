from django.db import models

class User(models.Model):
    email        = models.CharField(max_length = 50)
    password     = models.CharField(max_length = 300)
    name         = models.CharField(max_length = 50, null=True)
    phone_number = models.CharField(max_length = 50, null=True)
    created_at   = models.DateTimeField(auto_now_add = True)
    updated_at   = models.DateTimeField(auto_now = True)
