from django.db              import models
from django.core.exceptions import MultipleObjectsReturned

class User(models.Model):
     name       = models.CharField(max_length=30, unique=True, default='')
     password   = models.CharField(max_length=100)

     class Meta:
         db_table = 'users'


