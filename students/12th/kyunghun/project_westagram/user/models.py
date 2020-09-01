from django.db import models


class Users(models.Model):
    name              = models.CharField(max_length = 50)
    email             = models.CharField(max_length = 50)
    password          = models.CharField(max_length = 300)
    phon_number       = models.CharField(max_length = 100, null = True)
    created_at        = models.DateTimeField(auto_now_add = True) # 생성된 시간
    updated_at        = models.DateTimeField(auto_now = True) # 정보가 update 된 시간