from django.db import models


class User(models.Model):
  name         = models.CharField(max_length=45, null=True)
  phone_number = models.IntegerField(null=True)
  email        = models.EmailField(max_length=245)
  password     = models.CharField(max_length=300)

  class Meta:
    db_table = 'users'


