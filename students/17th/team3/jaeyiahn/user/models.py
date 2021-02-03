from django.db import models

class User(models.Model):
    username   = models.CharField(max_length=45, null=True, unique=True)
    phone      = models.CharField(max_length=45, null=True, unique=True)
    email      = models.EmailField(max_length=100, unique=True)
    password   = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

