from django.db import models

class User(models.Model):
    name       = models.CharField(max_length = 50, null=True)
    phone_num  = models.IntegerField()
    email      = models.CharField(max_length = 100, null=True)
    pw         = models.CharField(max_length = 200)
