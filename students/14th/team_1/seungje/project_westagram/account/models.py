from django.db import models

class Account(models.Model):

    user_name = models.CharField(max_length=40,default='')
    user_number = models.IntegerField(default='')
    user_email = models.CharField(max_length=40,default='')

    user_password = models.CharField(max_length=40)

    class Meta:
        db_table = 'accounts'
