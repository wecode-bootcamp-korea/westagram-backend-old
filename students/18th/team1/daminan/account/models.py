from django.db import models

class User(models.Model):
    email    = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    follow   = models.ManyToManyField("self", symmetrical=False)
    
    class Meta:
        db_table = "users"
    