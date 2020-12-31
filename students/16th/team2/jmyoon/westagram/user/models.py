from django.db import models

class User(models.Model):
    email      = models.CharField(max_length = 40, unique = True)
    phone      = models.CharField(max_length = 40, unique = True)
    name       = models.CharField(max_length = 40)
    user_name  = models.CharField(max_length = 40, unique = True)
    password   = models.CharField(max_length = 200)
    
    class Meta :
        db_table = 'users'