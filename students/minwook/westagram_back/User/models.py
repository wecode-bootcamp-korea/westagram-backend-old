from django.db import models

class User(models.Model):
    name     = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50, null = False)
    email    = models.CharField(max_length = 50)
    phone    = models.CharField(max_length = 30)
