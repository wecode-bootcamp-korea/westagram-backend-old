import jwt
import bcrypt

from django.http import JsonResponse

from my_settings import SECRET, ALGO
from user.models import User
from user.const import UTF8

def authorization_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization", None)
            payload      = jwt.decode(
                access_token,
                SECRET['secret'],
                algorithms = ALGO
            )
            login_user   = User.objects.get(id=payload['id'])
            request.user = login_user
            
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"message": "NOT_EXIST_USER"}, status=400)
        
        return func(self, request, *args, **kwargs)
    
    return wrapper

def get_hashed_pw(password):
    return bcrypt.hashpw(password.encode(UTF8), bcrypt.gensalt())

def get_access_token(user_id):
    token = jwt.encode({'userID': user_id}, SECRET['secret'], algorithm=ALGO)
    return token.decode(UTF8)
