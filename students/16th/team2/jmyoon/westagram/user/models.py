from django.db import models

class Account(models.Model):
    email      = models.CharField(max_length = 40)
    name       = models.CharField(max_length = 40)
    phone      = models.CharField(max_length = 40)
    password   = models.CharField(max_length = 200)
    
    class Meta :
        db_table = 'accounts'