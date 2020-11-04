from django.db import models

class User(models.Model):
    user_name       = models.CharField(max_length=45,unique=True)
    email           = models.EmailField(max_length=254,unique=True)
    phone_number    = models.CharField(max_length=45,unique=True)
    password        = models.CharField(max_length=1000)

    class Meta:
        db_table = 'users'
