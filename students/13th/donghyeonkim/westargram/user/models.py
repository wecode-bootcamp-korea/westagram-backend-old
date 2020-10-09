from django.db import models

class User(models.Model):
    name = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=11, unique=True)

    class Meta:
        db_table = 'user'