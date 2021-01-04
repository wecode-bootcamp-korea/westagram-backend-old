import json
import jwt

from django.http import JsonResponse

from users.models import User
from my_settings import SECRET_KEY


def check_blank(func):
    def wrapper(self, request, *args, **kwargs):
        data        = json.loads(request.body)
        value_list  = data.values()
        if "" in value_list:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        return func(self, request, *args, **kwargs)
    return wrapper

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token    = json.loads(request.headers.get("Token"))
            jwt_user        = jwt.decode(access_token, SECRET_KEY, algorithms = "HS256")
            return func(self, request, *args, **kwargs)
        except jwt.DecodeError:
            return JsonResponse({"message":"JWT_INVALID"}, status = 401)
        except TypeError:
            return JsonResponse({"message":"LOGIN_REQUIRED"}, status = 401)
    return wrapper

def get_user(token):
    user_id = jwt.decode(token, SECRET_KEY, algorithms = "HS256").get("id")
    user    = User.objects.get(id = user_id)
    return user
