from django.db import models

class User(models.Model):
    email    = models.EmailField(max_length = 100)
    password = models.CharField(max_length = 200)

    class Meta:
        db_table = 'users'

