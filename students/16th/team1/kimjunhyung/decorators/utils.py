import json
import jwt

from django.http import JsonResponse
from django.db          import connection

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
            access_token    = request.META["HTTP_AUTHORIZATION"].strip('""')
            jwt_user        = jwt.decode(access_token , SECRET_KEY, algorithms = ["HS256"])
            user_id         = jwt_user.get("id")
            user            = User.objects.filter(id = user_id)
            if not user.exists():
                return JsonResponse({"message":"USER_DOES_NOT_EXIST"}, status = 400)
            request.user    = user[0]
            return func(self, request, *args, **kwargs)
        except jwt.DecodeError:
            return JsonResponse({"message":"JWT_INVALID"}, status = 401)
        except TypeError:
            return JsonResponse({"message":"LOGIN_REQUIRED"}, status = 401)
    return wrapper



