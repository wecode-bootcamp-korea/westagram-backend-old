from django.db import models

class Account(models.Model):
    name         = models.CharField(max_length = 200)
    password     = models.CharField(max_length = 200)
    email        = models.EmailField(max_length = 200)
    phone_number = models.CharField(max_length = 200)

    class Meta:
        db_table = 'account'

    
