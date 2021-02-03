import re

from django.http    import JsonResponse

MAXIMUM_EMAIL_LENGTH = 100
MINIMUM_PASSWORD_LENGTH = 8
MAXIMUM_PASSWORD_LENGTH = 24
MAXIMUM_ACCOUNT_LENGTH = 20
MINIMUM_MOBILE_LENGTH = 10
MAXIMUM_MOBILE_LENGTH = 15

def validate_length(data):
    if len(data['email']) > MAXIMUM_EMAIL_LENGTH or \
            len(data['password']) > MAXIMUM_PASSWORD_LENGTH:
                return False

    if data.get('account'):
        if len(data['account']) > MAXIMUM_ACCOUNT_LENGTH:
            return False

    return True

def validate_email(email):
    if '@' not in email or '.' not in email:
        return False
    return True

def validate_password(password):
    if len(password) < MINIMUM_PASSWORD_LENGTH:
        return False
    return True

def validate_account(account):
    if len(account) > MAXIMUM_ACCOUNT_LENGTH:
        return False
    return True

def validate_mobile(mobile):
    if len(mobile) > MAXIMUM_MOBILE_LENGTH:
        return False

    mobile_regex = r'[0-9]{' f'{MINIMUM_MOBILE_LENGTH}' r',}'
    if not re.compile(mobile_regex).match(mobile):
        return False
    
    return True
