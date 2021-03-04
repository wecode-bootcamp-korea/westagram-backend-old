from django.db import models
from django.core.validators import MinLengthValidator

password_validator = MinLengthValidator(8, "8자 이상의 비밀번호를 입력하세요.")

class User(models.Model):
    mobile_number = models.CharField(max_length=14)
    email = models.EmailField(max_length=100)
    full_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100, validators=[password_validator], null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'users'
