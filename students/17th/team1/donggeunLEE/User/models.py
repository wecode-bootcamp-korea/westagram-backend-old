from django.db import models

# Create your models here.

class Userinfo(models.Model):
    name         = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, unique=True, default = 0)
    email        = models.CharField(max_length=25, unique=True)
    password     = models.CharField(max_length=250, default=0)


    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'userinfo'
