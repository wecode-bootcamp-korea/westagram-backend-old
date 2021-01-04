from django.db import models

# Create your models here.

class User(models.Model):

    user_id  = models.CharField(max_length=10)
    password = models.CharField(max_length=100)
    nickname = models.CharField(max_length=20)
    name     = models.CharField(max_length=10, null=True)
    email    = models.EmailField(null=True)
    phone    = models.CharField(max_length=45, null=True)
    
    class Meta:
        db_table = "users"

        