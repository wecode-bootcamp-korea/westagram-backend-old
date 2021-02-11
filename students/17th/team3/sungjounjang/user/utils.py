import jwt
import json

from django.http  import JsonResponse
from django.conf  import settings

from user.models import Accounts
from my_settings import SECRET, ALGORITHM

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.header['Authorization']
            payload      = jwt.decode(access_token, SECRET, algorithms=ALGORITHM)
            user         = Accounts.objects.get(email=payload)
            reqeust.user = user
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=400)
        
        except Accounts.DoesNotExist:
            return JsonResponse({'message':'INVALID_ACCOUNT'}, status=400)
        return func(self, request, *args, **kwargs)

    return wrapper