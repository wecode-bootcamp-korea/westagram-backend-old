import jwt
import json
import requests

from django.http import HttpResponse

from user.models import User
import my_settings

def login_decorator(func):
    def wrapper(self,request,*args, **kwargs):
        try:
            token = request.headers['Authorization']
            payload = jwt.decode(token, my_settings.SECRET_KEY, algorithms=my_settings.ALGORITHM)
            user = User.objects.get(email=payload['email'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=400)
        return func(self, request, *args, **kwargs)

    return wrapper
