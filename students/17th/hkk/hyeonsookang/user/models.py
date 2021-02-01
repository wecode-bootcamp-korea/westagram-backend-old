from django.db import models

class User(models.Model):
    email       = models.CharField(max_length=300, unique=True)
    phonenumber = models.IntegerField(default=0, unique=True)
    account     = models.CharField(max_length=300, unique=True)
    password    = models.CharField(max_length=255)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Users'
