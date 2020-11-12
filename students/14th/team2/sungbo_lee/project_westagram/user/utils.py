import jwt

from django.http import JsonResponse

from project_westagram.settings import SECRET_KEY, ABC
from user.models                import User

def check_user(func):
    def wrapper_func(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)

        if not access_token:
            return JsonResponse({"message": "NO_TOKENS"}, status=400)

        try:
            token        = jwt.decode(access_token, SECRET_KEY, algorithm=ABC)
            user         = User.objects.get(id=token["id"])
            request.user = user.id

        except User.DoesNotExist:
            return JsonResponse({"message": "unknown_user"}, status=401)

        except jwt.DecodeError:
            return JsonResponse({"message": "invalid_token"}, status=401)

        return func(self, request, *args, **kwargs)

    return wrapper_func
