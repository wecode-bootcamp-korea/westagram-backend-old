from django.db import models

class User(models.Model): 
    email    = models.EmailField()
    phone    = models.CharField(max_length=20)
    name     = models.CharField(max_length=20)
    password = models.CharField(max_length=1000)
    follow   = models.ManyToManyField("self", symmetrical=False)
    
    class Meta: 
        db_table = 'users'