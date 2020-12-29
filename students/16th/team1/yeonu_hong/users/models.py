from django.db import models

# Create your models here.

class User(models.Model):
    name     = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    phone    = models.IntegerField()
    email    = models.EmailField()

    class Meta:
        db_table = 'users'