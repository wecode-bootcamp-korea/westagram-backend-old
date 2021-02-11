import jwt, json, requests

from functools              import wraps
from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from westagram.settings import SECRET_KEY
from .models            import User

def login_required(func):
    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authrozation', None)
            payload      = jwt.decode(access_token, SECRET_KEY, algorithms = 'HS256')
            user         = User.objects.get(email = payload['email'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID TOKEN'}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({'message' : 'THIS ACCOUNT DOES NOT EXIST'}, status = 400)

        return func(self, request, *args, **kwargs)
    return wrapper
            