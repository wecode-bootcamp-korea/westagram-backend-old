from django.db import models

class User(models.Model):
    account  = models.CharField(max_length=6)
    password = models.CharField(max_length=8)

    class Meta:
        db_table = 'users'

