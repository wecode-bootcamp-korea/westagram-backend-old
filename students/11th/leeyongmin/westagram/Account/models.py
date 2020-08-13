from django.db import models

class User(models.Model):
    email    = models.CharField(max_length=100) # 휴대번호 또는 이메일
    name     = models.CharField(max_length=100) # 성명
    username = models.CharField(max_length=100) # 사용자이름(id)
    password = models.CharField(max_length=400) # 비밀번호