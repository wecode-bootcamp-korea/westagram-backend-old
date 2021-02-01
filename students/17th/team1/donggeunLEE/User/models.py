from django.db import models
from django.db.models.constraints import UniqueConstraint

# Create your models here.

class Userinfo(models.Model):
    name         = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    email        = models.CharField(max_length=25, unique=True)
    password     = models.CharField(max_length=25, default=0)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'userinfo'
