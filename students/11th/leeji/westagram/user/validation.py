import re

from django.core.exceptions import ValidationError

def Validate_email(value):
    email_reg = r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
    regex = re.compile(email_reg)

    if not regex.match(value):
        raise ValidationError('이메일 형식을 맞춰주세요')
    
def Validate_password(password):
    if len(password) <= 8:
        raise ValidationError('비밀번호를 8자 이상을 입력하세요.')

def Validation_phone(phone):
    if len(phone) != 11:
        raise ValidationError('핸드폰번호는 11자리입니다.')

