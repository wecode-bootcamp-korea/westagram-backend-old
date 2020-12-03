from django.db import models

# Create your models here.

class Users(models.Model):
    
    email = models.EmailField(max_length = 128,
                                verbose_name = "사용자 이메일"
                                )
    password = models.CharField(max_length = 64,
                                verbose_name = "사용자 비밀번호"
                                )

    class Meta:

        db_table = "Users"
