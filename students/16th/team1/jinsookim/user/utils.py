import jwt
import json
from django.http import JsonResponse
from westagram.settings import SECRET

from user.models import Users
from posting.models import Post_register


def login_decorator(func): 
    def wrapper(self, request, *args, **kwargs):
        try:
            token    = request.headers.get("Authorization")
            jwt_user = jwt.decode(token, SECRET, algorithms="HS256")

        except jwt.exceptions.InvalidSignatureError:
            return JsonResponse({"message :" : "잘못된 유저입니다"}, status=400)
            
        except jwt.exceptions.DecodeError:
            return JsonResponse({"message :" : "잘못된 유저입니다"}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper

