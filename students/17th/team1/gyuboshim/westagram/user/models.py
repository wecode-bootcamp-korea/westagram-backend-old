from django.db import models

class User(models.Model):
    phone_number    =   models.CharField(max_length = 15)
    email_adress    =   models.CharField(max_length = 100)
    name            =   models.CharField(max_length = 50)
    nickname        =   models.CharField(max_length = 50)
    password        =   models.CharField(max_length = 300)

    class Meta:
        db_table = 'user'
