import jwt
import json
import requests

from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from my_settings import SECRET_KEY,ALGORITHM
from user.models import User


email_regex    = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
password_regex = '[A-Za-z0-9@#$]{8,12}'

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token        = request.headers.get("Authorization")
            payload      = jwt.decode(token, SECRET_KEY, ALGORITHM)
            user         = User.objects.get(id=payload['id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN' }, status=401)
        
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)
        
        return func(self, request, *args, **kwargs)

    return wrapper