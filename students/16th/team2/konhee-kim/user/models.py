from django.db import models

class User(models.model)
    email         = models.EmailField(unique=True, blank=True)
    mobile_number = models.IntegerField(unique=True, null=True)
    full_name     = models.CharField(max_length=50, blank=True)
    username      = models.CharField(max_length=50, blank=True)
    password      = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'

