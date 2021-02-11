from django.db import models

# autopep8: off
class Users(models.Model):
    email        = models.EmailField(max_length=254)
    password     = models.CharField(max_length=600)
    name         = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
