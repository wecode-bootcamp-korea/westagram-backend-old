from django.db import models


class User(models.Model):
    account = models.CharField(max_length = 100) 
    password = models.CharField(max_length = 20)
    class Meta:
        db_table = 'users'
