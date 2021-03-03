from django.db import models


class User(models.Model):
  name         = models.CharField(max_length=45)
  user_name    = models.CharField(max_length=45, unique=True)
  phone_number = models.IntegerField(unique=True)
  email        = models.EmailField(max_length=245, unique=True)
  password     = models.CharField(max_length=300)
  
  class Meta:
    db_table = 'users'


