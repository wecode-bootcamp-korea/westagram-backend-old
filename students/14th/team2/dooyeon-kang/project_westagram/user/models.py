from django.db import models

class User(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=30)

    class Meta:
        db_table = 'users'
