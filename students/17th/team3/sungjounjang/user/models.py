from django.db import models

class Accounts(models.Model):
    email        = models.EmailField(max_length=100)
    name         = models.CharField(max_length=50)
    nickname     = models.CharField(max_length=50)
    password     = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)

    class Meta:
        db_table = "accounts"

