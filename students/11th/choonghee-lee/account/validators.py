import json
import re

from .codes import (
    ERROR_INVALID_INPUT,
    ERROR_INVALID_PHONE,
    ERROR_INVALID_EMAIL,
    SUCCESS_VALID_REQUEST,
)

KEY_PHONE_OR_EMAIL  = 'phone_or_email'
KEY_NAME            = 'name'
KEY_USERNAME        = 'username'
KEY_PASSWORD        = 'password'

def is_valid_name(name):
    REGEX_USERNAME = '^[a-zA-Z0-9]{2,30}$'
    result = False

    if not name:
        return result
    if re.search(REGEX_USERNAME, name):
        result = True
    
    return result

def is_valid_username(username):
    REGEX_USERNAME = '^[a-zA-Z0-9]{6,30}$'
    result = False

    if not username:
        return result
    if re.search(REGEX_USERNAME, username):
        result = True
    
    return result

def is_valid_email(email):
    REGEX_EMAIL = '^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$'
    result = False

    if not email:
        return result
    if re.search(REGEX_EMAIL, email):
        result = True

    return result

def is_valid_phone_number(phone_number):
    # TODO: support world wide phone numbers
    REGEX_PHONE_NUMBER = '^\d{3}\d{3,4}\d{4}$'
    result = False

    if not phone_number:
        return result
    if re.search(REGEX_PHONE_NUMBER, phone_number):
        result = True

    return result

def is_valid_password(password):
    REGEX_PASSWORD = '^[a-zA-Z0-9@#$%^&+=]{8,128}$'
    result = False

    if not password:
        return result

    if re.search(REGEX_PASSWORD, password):
        result = True

    return result

def is_number_string(number_string):
    REGEX_ONLY_NUMBER = '^\d+$'
    result = False

    if not number_string:
        return result

    if re.search(REGEX_ONLY_NUMBER, number_string):
        result = True

    return result

class UserRegisterValidator:
    def __init__(self, post):
        self.post = post

    def __call__(self, request, **kwargs):
        result_code = SUCCESS_VALID_REQUEST
        phone_or_email = ''
        name = ''
        username = ''
        password = ''

        json_data = json.loads(request.body)
        try:
            phone_or_email = json_data[KEY_PHONE_OR_EMAIL]
            name = json_data[KEY_NAME]
            username = json_data[KEY_USERNAME]
            password = json_data[KEY_PASSWORD]
        except KeyError:
            result_code = ERROR_INVALID_INPUT

        if (not is_valid_name(name) or
            not is_valid_username(username) or
            not is_valid_password(password)):
            result_code = ERROR_INVALID_INPUT
        if (not is_valid_email(phone_or_email) and 
            not is_valid_phone_number(phone_or_email)):
            if is_number_string(phone_or_email):
                result_code = ERROR_INVALID_PHONE
            else:
                result_code = ERROR_INVALID_EMAIL

        return self.post(
            self, 
            request,
            **{
                'phone_or_email': phone_or_email,
                'name': name,
                'username': username,
                'password': password,
                'result_code': result_code,
            },
         )