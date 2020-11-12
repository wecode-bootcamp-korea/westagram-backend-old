import jwt
import re
import json

from django.http import JsonResponse

from my_settings import SECRET_KEY
from user.models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            print(access_token)
            payload = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')
            user = User.objects.get(id=payload['id'])
            request.user=user
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper


def validate_email(email):
    return re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z]+\.[a-z.]+$', email)

def validate_password(password):
    return len(password) > 5

def validate_phone_number(phone_number):
    return re.match('^[0-9]{3}-[0-9]{3,4}-[0-9]{4}$', phone_number)


