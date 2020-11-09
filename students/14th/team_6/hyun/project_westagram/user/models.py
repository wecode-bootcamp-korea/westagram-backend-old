from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=20)
    user_phone_number = models.IntegerField()
    user_email = models.EmailField()
    user_password = models.CharField(max_length=20)

    class Meta :
        db_table = 'users'


