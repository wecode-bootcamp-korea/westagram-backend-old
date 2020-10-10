from django.db import models

class User(models.Model):
    password     = models.CharField(max_length=40)
    user_name    = models.CharField(max_length=40)
    email        = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=40)

    class Meta :
        db_table = 'user'