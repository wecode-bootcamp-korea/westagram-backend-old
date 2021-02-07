import json
import jwt

from django.http           import JsonResponse

from westagram.my_settings import ALGORITHM, SECRET
from . models              import User


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers['authorization']
            payload      = jwt.decode(access_token, SECRET, algorithms=ALGORITHM)
            user         = User.objects.get(id=payload['user-id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper
