import jwt
import my_settings
from functools   import wraps

from django.http import JsonResponse
from django.conf import settings

from .models     import User

def login_required(func) :
    @wraps(func)
    def wrapper(self, request, *args, **kwargs) :

        try:
           if 'Authentication' not in request.headers:
               return JsonResponse({"message" : "Unauthorized"}, status = 401)

           access_token = request.headers.get('Authorization')

           key          = settings.SECRET_KEY
           algorithm    = settings.ALGORITHM
           data         = jwt.decode(access_token, key, algorithm)

           user_id      = User.objects.get(id = data["user"])
           request.user = user_id

        except jwt.DecodeError:
            return JsonResponse({"message" : "TOKEN_ERROR"}, status = 401)

        except User.DoesNotExist :
            return JsonResponse({"message" : "USER_NOT_EXIST"}, status = 401)

        return func(self, request, *args, **kwargs)

    return wrapper
