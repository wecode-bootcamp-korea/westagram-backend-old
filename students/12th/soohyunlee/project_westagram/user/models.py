from django.db import models

class User:
    name       = models.CharField(max_length = 50)
    phone_num  = models.CharField(max_length = 50)
    email      = models.CharField(max_length = 100)
    pw         = models.CharField(max_length = 200)
# Create your models here.
