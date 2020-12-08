from django.db import models

class User(models.Model):
    user_name = models.CharField(max_length=70)
    password = models.CharField(max_length=100)
#    phonenumber = models.CharField(max_length=13)
#    email = models.CharField(max_length=70)

    class Meta:
        db_table = 'users'

