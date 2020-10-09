from django.db import models

class User(models.Model):
    name     = models.CharField(max_length=50, unique=True)
    account  = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = 'user'