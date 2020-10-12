from django.db import models

class User(models.Model):
    name            = models.CharField(max_length = 20)
    phone_number    = models.CharField(max_length = 20)
    email           = models.EmailField(max_length = 75)
    password        = models.CharField(max_length = 20)
    
    class Meta:
        db_table = 'users'
