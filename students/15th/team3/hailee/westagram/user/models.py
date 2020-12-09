from django.db import models

# Create your models here.
class User(models.Model):
     user_name   = models.CharField(max_length=30)
     #email       = models.CharField(max_length=40)
     #phone_number= models.CharField(max_length=30)
     password    = models.CharField(max_length=30)

     class Meta:
         db_table = 'users'


# class
