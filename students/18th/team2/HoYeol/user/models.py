from django.db import models

class User(models.Model):

    email   = models.EmailField(max_length=50, unique=True)
    password= models.CharField(max_length=500)
    
    # name    = models.CharField(max_length=50, unique=True, null=True)
    # phone   = models.CharField(max_length=50, unique=True, null=True)
   

    class Meta:
        db_table='users'

