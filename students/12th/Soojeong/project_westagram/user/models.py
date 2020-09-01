from django.db import models

# Create your models here.
class UserManager(models.Model):
    login_name              = models.CharField(max_length=50)
    phone_number_or_email   = models.CharField(max_length=12)
    password                = models.CharField(max_length=50)
    name                    = models.CharField(max_lenghth=50)
    