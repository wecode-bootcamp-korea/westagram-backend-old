import jwt
import json
from functools import wraps

from django.http import JsonResponse

from user.models import User
from westagram.settings import SECRET_KEY

def id_auth(func):
    @wraps(func)
    def decorated_function(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            payload      = jwt.decode(access_token, SECRET_KEY, algorithm = 'HS256')
            login_user   = User.objects.get(id = payload['user_id'])
            request.user = login_user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status = 400)
        return func(self, request, *args, **kwargs)
    return decorated_function
