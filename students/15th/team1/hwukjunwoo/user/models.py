from django.db import models

class User(models.Model):
    name = models.CharField(max_length =50, null=True)
    phone = models.CharField(max_length =100, null=True)
    email = models.EmailField(max_length =200, null=True)
    password = models.CharField(max_length = 100)
    
    class meta:
        db_table = 'users'
