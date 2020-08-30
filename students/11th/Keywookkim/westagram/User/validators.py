from django.core.exceptions import ValidationError

def validate_email(email):
    if not '@' in email or not '.' in email :
        raise ValidationError(("Invalid email"), code='invalid')

def validate_password(password):
    if len(password) < 8 :
        raise ValidationError(("The length of password should be more than 8"), code='invalid')


# 람다로 정리 10개 ...포문
