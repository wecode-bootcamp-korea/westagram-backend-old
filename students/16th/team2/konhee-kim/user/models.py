from django.db import models

class User(models.Model):
    email         = models.EmailField(unique=True)
    mobile_number = models.CharField(blank=True, max_length=11)
    full_name     = models.CharField(max_length=50, blank=True)
    username      = models.CharField(max_length=50, unique=True)
    password      = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'

