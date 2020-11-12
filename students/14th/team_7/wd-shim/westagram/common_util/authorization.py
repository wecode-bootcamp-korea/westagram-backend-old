import jwt
import bcrypt

from django.http import JsonResponse

from my_settings import SECRET, ALGO
from user.const import UTF8
from user.models import User

def check_valid_user(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get("Authorization", None)
            print("access_token====================================")
            payload      = jwt.decode(
                access_token,
                SECRET['secret'],
                algorithms = ALGO
            )
            print("payload=========================================")
            
            login_user   = User.objects.get(id=payload['userID'])
            print("login_user_valid================================")
            request.user = login_user
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message": "401 UNAUTHORIZED"}, status=401)
        
        except User.DoesNotExist:
            return JsonResponse({"message": "NOT_EXIST_USER"}, status=400)
        
        return func(self, request, *args, **kwargs)
    
    return wrapper

def get_hashed_pw(password):
    return bcrypt.hashpw(password.encode(UTF8), bcrypt.gensalt()).decode(UTF8)

def get_access_token(user_id):
    token = jwt.encode({'userID': user_id}, SECRET['secret'], algorithm=ALGO)
    return token.decode(UTF8)