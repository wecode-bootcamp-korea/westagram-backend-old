import jwt
import json
from westagram.settings import SECRET
from user.models import Users
from posting.models import Post_register
from django.http import JsonResponse

def login_decorator(func): 
    def wrapper(self, request, *args, **kwargs):
        try:
            token = request.headers.get("Token")
            jwt_user = jwt.decode(token, SECRET, algorithms="HS256")

        except jwt.exceptions.InvalidSignatureError:
            return JsonResponse({"message :" : "token값이 잘못되었습니다."}, status=400)

        except Post_register.DoesNotExist:
            return JsonResponse({"message :" : "해당 게시물이 없습니다."}, status=401)

        except Users.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_USER"}, status = 400)

        except TypeError:
            return JsonResponse({"message :":"LOGIN Required"}, status = 400)

        except KeyError:
            return JsonResponse({'MESSAGE :':"KeyError"},status = 400)

        return func(self, request, *args, **kwargs)

    return wrapper

