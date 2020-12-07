from django.db import models
class User(models.Model):
    username       = models.CharField(max_length=50, null=True, blank=True)
    email          = models.CharField(max_length=50, null=True, blank=True)
    phone_number   = models.CharField(max_length=15, null=True, blank=True)
    password       = models.CharField(max_length=50)

    class Meta:
        db_table = 'users'
