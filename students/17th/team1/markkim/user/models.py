from django.db import models

class User(models.Model):
    full_name    = models.CharField(max_length=30)
    email        = models.EmailField()
    phone_number = models.CharField(max_length=30)
    username     = models.CharField(max_length=20)
    password     = models.CharField(max_length=300)

    class Meta:
        db_table = 'users'



