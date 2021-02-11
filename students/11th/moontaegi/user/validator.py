from django.core.exceptions import ValidationError

def validate_email(value):
    if not '@' in value or not '.' in value:
        raise ValidationError(("Invalid email"), code = 'invalid')

def validate_password(value):
    if len(value) < 8:
        raise ValidationError(("Too short password"), code = 'invalid')
    
