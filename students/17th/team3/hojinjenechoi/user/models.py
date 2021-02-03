from django.db import models

class User(models.Model):
    email           = models.EmailField(max_length=200, unique=True, verbose_name='Username')
    password        = models.CharField(max_length=300, verbose_name='Password') 
    nickname        = models.CharField(max_length=50)
    phone           = models.CharField(null=True, max_length=15)
    registered_time = models.DateTimeField(auto_now_add=True)
    updated_time    = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
    
   
