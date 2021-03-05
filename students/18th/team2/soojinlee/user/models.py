from django.db import models


class User (models.Model):
    email = models.CharField(max_length=400)
    pw = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)

    class Meta:
        db_table = 'users'
