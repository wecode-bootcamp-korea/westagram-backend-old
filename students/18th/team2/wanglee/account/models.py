from django.db import models

class User(models.Model):
    email     = models.EmailField(max_length=50, unique = True)
    password  = models.CharField(max_length=500)
    username  = models.CharField(max_length=50, unique = True)
    phone_num = models.CharField(max_length=50, unique = True)

    class Meta:
        db_table  = 'users'