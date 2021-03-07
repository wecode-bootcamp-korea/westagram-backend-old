from django.db import models

class User(models.Model):
    email    = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'users'
