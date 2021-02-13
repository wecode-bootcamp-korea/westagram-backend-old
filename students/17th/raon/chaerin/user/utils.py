import jwt
import json

from django.http   import JsonResponse

from .models       import Account
from my_settings   import SECRET

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):

        if 'Authorization' not in request.headers:
            return JsonResponse({'MESSAGE': 'NEED_LOGIN'}, status=401)

        try:
            access_token = request.headers['Authorization']
            payload      = jwt.decode(access_token, 'secret', algorithms=['HS256'])
            login_user   = Account.objects.get(id = payload['id'])
            request.user = login_user
            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN'}, status=401)

        except Account.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

    return wrapper
