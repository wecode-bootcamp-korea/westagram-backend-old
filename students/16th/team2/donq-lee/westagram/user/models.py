from django.db import models

class User(models.Model):
    email    = models.EmailField(max_length=200)
    name     = models.CharField(max_length=200)
    nickname = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

    class Meta:
        db_table = 'users'

