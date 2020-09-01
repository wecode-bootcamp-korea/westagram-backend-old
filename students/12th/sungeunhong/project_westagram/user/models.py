from django.db import models # ORM을 하기 위해 models import

class Users(models.model):
    name           = models.CharField(max_length = 50)
    phone_number   = models.CharField(max_length = 50) 
    email          = models.EmailField(max_length = 100)
    password       = models.CharField(max_length = 300)
    created_at     = models.DateTimeField(auto_now_add = True) # 최초 데이터 입력 시간 지정 
    updated_at     = models.DateTimeField(auto_now = True) # 업데이트 시 수정 시간 
    
    class Meta:
        db_table  = 'Users'
