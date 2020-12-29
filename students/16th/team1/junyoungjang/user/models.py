from django.db import models

class User(models.Model):
    name        = models.CharField(max_length  = 20)
    email       = models.EmailField(max_length = 100)
    password    = models.CharField(max_length  = 30)
    nickname    = models.CharField(max_length  = 150)
    phonenumber = models.CharField(max_length  = 15)

    class Meta:
        db_table = "users"