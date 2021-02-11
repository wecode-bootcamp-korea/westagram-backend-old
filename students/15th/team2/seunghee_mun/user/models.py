from django.db import models

class User(models.Model):
    user_name = models.CharField(max_length=70)
    password  = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'

