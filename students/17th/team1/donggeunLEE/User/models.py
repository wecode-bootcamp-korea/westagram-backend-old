from django.db import models

# Create your models here.

class Userinfo(models.Model):
    name         = models.CharField(max_length=20)
    Phone_number = models.CharField(max_length=15)
    email        = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'userinfo'

class UserPassword(models.Model):
    password     = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.password}'

    class Meta:
        db_table ='userpassword'
