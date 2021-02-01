from django.db import models

class User(models.Model):
    username   = models.CharField(max_length=45, null=True)
    password   = models.CharField(max_length=500)
    phone      = models.CharField(max_length=45, null=True)
    email      = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

