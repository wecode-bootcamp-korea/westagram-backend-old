from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=10)
    mail = models.EmailField(required=True)
    password = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'

