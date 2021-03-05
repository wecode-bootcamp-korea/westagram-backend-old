from django.db import models

class User(models.Model):
    email         = models.EmailField(max_length=50, unique=True)
    phone         = models.CharField(max_length=11, null=True, unique=True)
    full_name     = models.CharField(max_length=40, null=True)
    user_name     = models.CharField(max_length=20, null=True, unique=True)
    password      = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True)

    class Meta:
        db_table = 'users'
