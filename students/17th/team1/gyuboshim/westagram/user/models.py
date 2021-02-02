from django.db import models

class User(models.Model):
    phone_number    =   models.CharField(max_length = 15)
    email_adress    =   models.CharField(max_length = 50)
    name            =   models.CharField(max_length = 10)
    nickname        =   models.CharField(max_length = 10)
    password        =   models.CharField(max_length = 15)

    class Meta:
        db_table = 'user'
