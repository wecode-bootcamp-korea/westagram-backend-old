from django.db import models

class User(models.Model):
    name     = models.CharField(max_length=15)
    phone    = models.CharField(max_length=12)
    email    = models.EmailField() 
    password = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'



