from django.db import models

# Create your models here.

class User(models.Model):

    username    = models.CharField(max_length=45, null=True)
    email       = models.EmailField(null=True)
    phone       = models.CharField(max_length=45, null=True)
    password    = models.CharField(max_length=100)
    
    class Meta:
        db_table = "users"

        