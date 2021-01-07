import json
import re 

from django.http import JsonResponse
import bcrypt
import jwt

import my_settings

def hash_password(str_password):
    hashed_password = bcrypt.hashpw(
            str_password.encode('utf-8'), 
            bcrypt.gensalt()
            )
    return hashed_password.decode('utf-8')

def check_password(password, hashed_password):
    password        = password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password, hashed_password)

def generate_access_token(user_id_number):
    payload = {
            'user_id' : user_id_number  # exp shall be added
            }
    access_token = jwt.encode(payload, my_settings.SECRET, algorithm = 'HS256')
    return access_token

def login_required(function):    # use it as decorator 
    
    def wrapper(arg, request):   # to be tested
        headers      = json.loads(request.headers)
        access_token = headers['Authorization'] # consider bearer later
        header = jwt.decode(access_token, my_settings.SECRET, algorithms = 'HS256')

        try:
            if access_token:
                return function(arg, request)

            if not access_token:
                return JsonResponse({'MESSAGE': 'LOGIN_REQUIRED'}, status=400)
        except:
                return JsonResponse({'MESSAGE': 'LOGIN_REQUIRED'}, status=400)

    return wrapper

def validate_email(email):
    """
    for email validation. check email_addresss whether include '@' & '.'
    """
    try:
        return re.match(r".+@.+\..+", email).group(0) == email
    except:
        return False
    
def validate_mobile(mobile):
    """
    for mobile_number validation. 
    """
    try:
        return re.match(
                r"^01[0-9]-?[0-9][0-9][0-9][0-9]-?[0-9][0-9][0-9][0-9]$", mobile
                ).group(0) == mobile
    except:
        return False

def validate_password(password):
    """
    for password validation. check password > 8 characters
    """
    return re.match(r".*", password).span()[1] >= 8  


