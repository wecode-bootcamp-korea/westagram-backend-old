import  jwt
import  json
import  requests

from django.http  import JsonResponse
from django.conf  import settings
from user.models  import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers['Authorization']
            payload      = jwt.decode(access_token, settings.SECRET_KEY, algorithms=ALGORITHM)
            user         = User.objects.get(id=payload['id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({"message" : "INVALID_TOKEN"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=400)
        return func(self, request, *args, **kwargs)

    return wrapper
