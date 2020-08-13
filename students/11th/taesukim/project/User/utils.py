import jwt
import json

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from project.my_settings import SECRET_KEY
from User.models import User

def validate_token(func):
    def wrapper(self, request, *arg, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            header = jwt.decode(access_token, SECRET_KEY, algorithm = 'HS256')
            user = User.objects.get(id = header['id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status = 400)

        return func(self, request, *arg, **kwargs)

    return wrapper

