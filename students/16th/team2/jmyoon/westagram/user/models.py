from django.db import models

class User(models.Model):
    email      = models.EmailField(max_length = 40, null=True)
    phone      = models.CharField(max_length = 11, null=True)
    name       = models.CharField(max_length = 40)
    username  = models.CharField(max_length = 40)
    password   = models.CharField(max_length = 200)
    
    class Meta :
        db_table = 'users'