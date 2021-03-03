from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=128)
    password = models.CharField(max_length=50)
 