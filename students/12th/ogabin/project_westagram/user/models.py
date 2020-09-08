from django.db import models

class User(models.Model):
    name         = models.CharField(max_length = 20)
    email        = models.CharField(max_length = 20)
    password     = models.CharField(max_length = 8)
    phone        = models.CharField(max_length = 20)

    class Meta:
        db_table = 'users'