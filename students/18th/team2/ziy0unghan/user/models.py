from django.db import models

class User(models.Model):
    username     = models.CharField(max_length=45, unique=True)
    email        = models.EmailField(max_length=100, unique=True)
    password     = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=45, unique=True)

    class Meta:
        db_table='users'