from django.db import models

class Users(models.Model):
    
    email = models.EmailField(max_length = 128,
                                verbose_name = "사용자 이메일"
                                )
    password = models.CharField(max_length = 256,
                                verbose_name = "사용자 비밀번호"
                                )
    
    followers = models.ManyToManyField("self", related_name = "following",symmetrical=False)
    
    class Meta:

        db_table = "Users"


