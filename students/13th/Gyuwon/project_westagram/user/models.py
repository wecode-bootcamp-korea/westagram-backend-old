from django.db import models

class User(models.Model):
    name            = models.CharField(max_length = 20, unique = True)
    phone_number    = models.CharField(max_length = 20, unique = True)
    email           = models.EmailField(max_length = 75, unique = True)
    password        = models.CharField(max_length = 100)
    
    class Meta:
        db_table = 'users'
