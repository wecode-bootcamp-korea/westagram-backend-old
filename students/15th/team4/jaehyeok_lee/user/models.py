from django.db import models
from datetime import datetime

class User(models.Model):
    account  = models.CharField(max_length = 100)
    password = models.CharField(max_length = 1000)
    class Meta:
        db_table = 'users'
