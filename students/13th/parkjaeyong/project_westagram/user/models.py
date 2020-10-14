from django.db import models

class Users(models.Model):
    objects = models.Manager()
    name         = models.CharField(max_length=30)
    email        = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=100)
    password     = models.IntegerField()
    

    class Meta:
        db_table='user'





