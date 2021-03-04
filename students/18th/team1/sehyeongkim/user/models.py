from django.db import models

# Create your models here.

class User(models.Model):
    email = models.CharField(max_length= 130)
    password = models.CharField(max_length= 40)

    class Meta:
        db_table = 'users'

