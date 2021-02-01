from django.db import models

class User(models.Model):
    email        = models.EmailField(max_length=50, null=False, unique=True)
    password     = models.CharField(max_length=500, null=False)
    phone_number = models.CharField(max_length=50, null=False, unique=True)
    account      = models.CharField(max_length=50, null=False, unique=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'