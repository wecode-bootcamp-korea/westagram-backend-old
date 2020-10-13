from django.db import models

class User(models.Model):

    email        = models.CharField(max_length=100,null=True)
    phone_number = models.CharField(max_length=40,null=True)
    name         = models.CharField(max_length=40,null=True)    
    user_name    = models.CharField(max_length=40)
    password     = models.CharField(max_length=100)

    class Meta :
        db_table = 'user'