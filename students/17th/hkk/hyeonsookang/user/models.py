from django.db import models

class User(models.Model):
    email    = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    class Meta:
        db_table = 'Users'
