from django.db import models

class Users(models.Model):
    name  =models.CharField(max_length=30)
    tel   =models.CharField(max_length=100)
    email =models.EmailField(max_length=100)

    class Meta:
        db_table='user'