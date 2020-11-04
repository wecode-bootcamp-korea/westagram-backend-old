from django.db import models

# Create your models here.

# account 앱 생성 후 모델 작성

class Account(models.Model):
    username = models.CharField(max_length = 100)
    email    = models.CharField(max_length = 200)
    password = models.CharField(max_length = 500)
    phone    = models.CharField(max_length = 40)

    class Meta:
        db_table="accounts"



