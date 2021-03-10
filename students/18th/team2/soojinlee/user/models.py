from django.db import models


class User (models.Model):
    email = models.EmailField(unique=True, blank=False)
    password = models.CharField(max_length=100, blank=False)
    # user_name = models.CharField(max_length=100, unique=True, null=True)
    # phone_number = models.CharField(max_length=100, unique=True, null=True)

    class Meta:
        db_table = 'users'
