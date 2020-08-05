import re

from django.core.exceptions import ValidationError

def validate_email(value):
    pattern = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    if not pattern.match(value):
        raise ValidationError("INVALID_EMAIL")

def validate_number(value):
    pattern = re.compile("^\d{11}$")
    if not pattern.match(value):
        raise ValidationError("INVALID_PHONE_NUMBER")

def validate_password(value):
    if len(value) < 8:
        raise ValidationError("INVALID_PASSWORD")
