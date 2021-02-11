from django.db import models

class User(models.Model):
    username      = models.CharField(max_length=20, null=True)
    email         = models.EmailField(max_length=100, null=True)
    phonenumber  = models.CharField(max_length=20, null=True)
    password      = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'
