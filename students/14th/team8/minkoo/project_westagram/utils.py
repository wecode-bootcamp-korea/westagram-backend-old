import jwt
import json

from django.http                         import JsonResponse

from project_westagram.settings.settings import JWT_ALGORITHM, JWT_SECRET_KEY
from user.models                         import User

def login_decorator(func):
    def decorated_function(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            if not access_token:
                return JsonResponse({'message':'INVALID_USER'}, status=401)
            payload = jwt.decode(access_token, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
            user = User.objects.get(id=payload['user_id'])
            request.user_id = user.id
        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        return func(self, request, *args, **kwargs)
    return decorated_function
