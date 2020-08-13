from django.db import models

class Account(models.Model):
    name         = models.CharField(max_length = 200, help_text = "사용자 이름") # 사용자 이름
    phone_number = models.CharField(max_length = 200, help_text = "전화번호") # 전화번호
    email        = models.CharField(max_length = 200, help_text = "이메일") # 이메일
    password     = models.CharField(max_length = 400, help_text = "비밀번호") # 비밀번호
    created_date = models.DateTimeField(auto_now_add = True) # 처음 등록한 time 기록
    updated_date = models.DateTimeField(auto_now = True) # 수정한 time 기록
    # objects = models.Manager() 

    class Meta:
        db_table = "accounts"