from django.db import models

# Create your models here.
class User(models.Model):

    email   = models.CharField(max_length=50)
    name    = models.CharField(max_length=50)
    phone   = models.CharField(max_length=50)
    pswd    = models.CharField(max_length=50)

    class Meta:
        db_table='users'

