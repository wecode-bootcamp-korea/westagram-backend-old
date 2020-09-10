from django.db import models

class User(models.Model):
  email        = models.CharField(max_length = 50)
  name         = models.CharField(max_length = 50)
  password     = models.CharField(max_length = 300)
  phone_number = models.CharField(max_length = 100, null = True)
  created_at   = models.DateTimeField(auto_now_add = True)
  updated_at   = models.DateTimeField(auto_now = True)

  class meta:
    db_table = 'users'
