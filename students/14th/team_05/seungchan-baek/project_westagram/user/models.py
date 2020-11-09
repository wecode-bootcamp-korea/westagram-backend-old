from django.db import models

# Create your models here.

class User(models.Model):
    name         =   models.CharField(max_length=10)
    telephone    =   models.CharField(max_length=12)
    password     =   models.CharField(max_length=20)
    email        =   models.EmailField(max_length=20)


    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.name
