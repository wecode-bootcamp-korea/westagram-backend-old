import datetime
from django.db import models

# 사용자
class Users(models.Model):
    
    phone_number = models.CharField(max_length = 50 , null=True)
    user_name    = models.CharField(max_length = 50, null=True)
    email        = models.EmailField(max_length = 254, null=True)
    password     = models.BinaryField(max_length = 500)
    
    class Meta:
        db_table = 'users'


class Follow(models.Model):
    follower = models.ForeignKey('Users', on_delete = models.CASCADE, related_name='follower')
    followee = models.ForeignKey('Users', on_delete = models.CASCADE, related_name= 'floowee')

    class Meta:
        db_table = 'follow'