import jwt
import my_settings
from functools   import wraps

from django.http import JsonResponse
from django.conf import settings

from .models     import User

def login_required(func) :
    @wraps(func)
    def wrapper(self, request, *arg, **kwargs) :
        try:
            access_token = request.headers.get('Authorization', None)

            key          = settings.SECRET_KEY
            algorithm    = settings.ALGORITHM
            payload      = jwt.decode(access_token, key, algorithm)

            user_id      = User.objects.get(id = payload["id"])
            request.id   = user_id

        except Jwt.DecodeError :
            return JsonResponse({"message":"TOKEN_ERROR"}, status = 400)
        except User.DoesNotExist :
            return JsonResponse({"message":"USER_NOT_EXIST"}, status = 400)

        return(func)
    return wrapper
