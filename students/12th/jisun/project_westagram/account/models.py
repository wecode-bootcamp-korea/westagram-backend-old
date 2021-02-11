from django.db import models

class User(models.Model):
    email         = models.EmailField(max_length  = 20, null=True)
    password      = models.CharField(max_length  = 20)
    name          = models.CharField(max_length = 20)
    phone_numbers = models.CharField(max_length = 20, null=True)


