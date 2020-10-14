from django.db import models

class Users(models.Model):
    name    = models.CharField(max_length=30)
    tel     = models.CharField(max_length=100)
    email   = models.EmailField(max_length=100)
    password= models.IntegerField()

    class Meta:
        db_table='user'