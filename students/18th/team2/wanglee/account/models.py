from django.db import models

class User(models.Model):
    email     = models.EmailField(max_length=30)
    password  = models.CharField(max_length=500)
    username  = models.CharField(max_length=20)
    phone_num = models.CharField(max_length=20)

    class Meta:
        db_table  = 'users'