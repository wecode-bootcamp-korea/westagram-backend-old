from django.db import models

class Account(models.Model):
    name      = models.CharField(max_length=50)
    email     = models.CharField(max_length=50)
    password  = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=50)

    