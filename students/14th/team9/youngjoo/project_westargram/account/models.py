from django.db import models

class Accounts(models.Model):
    name         = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=30)
    email        = models.EmailField(max_length=50)
    password     = models.CharField(max_length=50)


