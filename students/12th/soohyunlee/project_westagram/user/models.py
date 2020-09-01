from django.db import models

class User:
    user_name = models.CharField(max_length = 50)
    user_num  = models.CharField(max_length = 50)
    user_mail = models.CharField(max_length = 100)
    user_pw   = models.CharField(max_length = 200)
# Create your models here.
