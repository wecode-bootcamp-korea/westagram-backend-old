from django.db import models

class User(models.Model):
    email         = models.CharField(max_length=100, unique=True, null=True)
    mobile_number = models.CharField(max_length=100, unique=True, null=True)
    full_name     = models.CharField(max_length=100)
    username      = models.CharField(max_length=100, unique=True)
    password      = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'

