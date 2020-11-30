import jwt
import json

from django.conf import settings
from django.http import JsonResponse

from .models     import User

def key_error_decorator(func):
    pass

def login_decorator(func):

    def wrapper(self, request, *args, **kwargs):
        if 'Authorization' not in request.headers:
            return JsonResponse({'message': 'DO_NOT_EXIST_TOKEN'}, status=401)

        try:
            encode_token = request.headers['Authorization'].encode('utf-8')
        except AttributeError:
            return JsonResponse({'message' : 'INVALID_TOKEN: TYPE_ERROR'}, status=401)


        try:
            decode_data = jwt.decode(encode_token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=decode_data['id'])
            request.user_id = user.id
        except (jwt.DecodeError, KeyError, AttributeError):
            return JsonResponse({'message' : f'INVALID_TOKEN:{decode_data}'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'DO_NOT_EXIST_USER'}, status=401)

        return func(self, request, *args, **kwargs)
    return wrapper
