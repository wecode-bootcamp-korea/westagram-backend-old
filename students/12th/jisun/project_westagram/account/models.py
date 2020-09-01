from django.db import models

class Users(models.Model):
    email         = models.EmailField(max_length  = 20)
    password      = models.CharField(max_length  = 20)
    name          = models.CharField(max_length = 20)
    phone_numbers = models.CharField(max_length = 20)


