from django.db import models


class User (models.Model):
    email        = models.EmailField(max_length=100, unique=True, blank=False)
    password     = models.CharField(max_length=100, blank=False)
    user_name    = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'users'
