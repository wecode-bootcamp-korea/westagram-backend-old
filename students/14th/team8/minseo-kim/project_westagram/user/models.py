from django.db import models


class User(models.Model):
    name      = models.CharField(max_length=20)
    email     = models.EmailField()
    password  = models.CharField(max_length=100)
    number    = models.IntegerField()

    class Meta:
        db_table = 'users'
