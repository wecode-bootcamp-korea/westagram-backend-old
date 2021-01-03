from django.db import models
from django.conf import settings

class User(models.Model):
    account = models.CharField(max_length = 20)
    password = models.CharField(max_length= 30)
    email = models.EmailField(max_length = 30)
    tel_num = models.CharField(max_length = 20)
    created_time = models.DateTimeField(auto_now_add = True)
    updated_time = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.account

    class Meta:
        db_table = 'users'

