from django.db import models

class User(models.Model):
    username     = models.CharField(max_length=50, unique=True)
    email        = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=50, unique=True, null=True)
    password     = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'users'
