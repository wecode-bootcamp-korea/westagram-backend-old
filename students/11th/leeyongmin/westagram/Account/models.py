import datetime

from django.db import models
from django.utils import timezone


class User(models.Model):
    name        = models.CharField(max_length=100) 
    email       = models.CharField(max_length=100) 
    password    = models.CharField(max_length=100)
    phone       = models.CharField(max_length=50)
