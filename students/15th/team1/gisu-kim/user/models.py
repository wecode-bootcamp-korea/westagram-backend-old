from django.db import models

# Create your models here.

class Users(models.Model) : 
#    name      = models.CharField(
#            max_length=20, verbose_name = '사용자 이름'
#            )
#    phone     = models.CharField(
#            max_length=30, verbose_name = '전화번호'
#            )
    email     = models.CharField(
            max_length=50, verbose_name = '이메일 주소'
            )
    password  = models.CharField(
            max_length=60, verbose_name = '비밀번호'
            )

    class Meta : 
        db_table = 'Users'

    
