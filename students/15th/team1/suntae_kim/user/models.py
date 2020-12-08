from django.db import models


# 코드 작성

class User(models.Model):
#    mobile_email = models.CharField(max_length=45)
#    fullname     = models.CharField(max_length=45)
    username     = models.CharField(max_length=45)
    password     = models.CharField(max_length=150)
    class Meta:
        db_table = 'users'
