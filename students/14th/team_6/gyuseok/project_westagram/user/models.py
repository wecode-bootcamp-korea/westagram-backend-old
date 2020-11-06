from django.db import models

# Create your models here.
class User(models.Model):
    name          = models.CharField(max_length=100)
    phone_number  = models.CharField(max_length=100)
    email         = models.CharField(max_length=100)
    password      = models.CharField(max_length=100)
    class Meta:
        db_table = 'user' # 이러면 테이블에 데이터베이스 명이 붙지 않는다.

    def __str__(self): # 클래스 호출 시 name을 출력 
        return self.name

