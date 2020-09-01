from django.db import models

class User(models.Model):
    name       = models.CharField(max_length = 50)
    phone_num  = models.IntegerField()
    email      = models.CharField(max_length = 100)
    pw         = models.CharField(max_length = 200)