from django.db import models

# Create your models here.


class User(models.Model):
    name     = models.CharField(max_length=45,unique=True)
    phone    = models.CharField(max_length=30,unique=True)
    email    = models.EmailField(max_length=254,unique=True)
    password = models.CharField(max_length=25)

    class Meta:
        db_table = 'users'
