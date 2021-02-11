import jwt
import json

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from my_db_settings import SECRET_KEY, ALGORITHM
from user.models import User

def login_check(func):

    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload = jwt.decode(access_token, SECRET_KEY, algorithm=ALGORITHM)
            user_id = User.objects.get(id=payload['id'])
            request.user = user_id

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID TOKEN'}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID USER'}, status = 400)

        return func(self, request, *args, **kwargs)

    return wrapper
