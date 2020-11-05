from django.db import models

# Create your models here.

class Users(models.Model):
    user_name       = models.CharField(max_length=30)
    phone_number    = models.CharField(max_length=30)
    email           = models.EmailField(max_length=30)
    password        = models.CharField(max_length=20)
    class Meta:
        db_table    = 'users_info'
