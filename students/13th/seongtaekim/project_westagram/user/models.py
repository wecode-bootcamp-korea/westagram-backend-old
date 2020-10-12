from django.db import models

class User(models.Model):
    email        = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=40)
    name         = models.CharField(max_length=40)    
    user_name    = models.CharField(max_length=40)
    password     = models.CharField(max_length=40)

    class Meta :
        db_table = 'user'

