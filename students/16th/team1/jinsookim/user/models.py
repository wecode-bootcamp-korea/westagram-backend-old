import datetime
from django.db import models

# 사용자
class Users(models.Model):
    
    phone_number = models.CharField(max_length = 50)
    user_name    = models.CharField(max_length = 50)
    email        = models.EmailField(max_length = 254)
    password     = models.BinaryField(max_length = 500)
    
    class Meta:
        db_table = 'users'




