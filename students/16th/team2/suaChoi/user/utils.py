import jwt

from django.http import JsonResponse

from westagram.settings import SECRET
from user.models        import User
from posting.models     import Post

def check_user(func):
    def wrapper(self, request, *args, **kwargs):

        try:
            token        = request.headers.get('Authorization')
            payload      = jwt.decode(token, SECRET, algorithms='HS256')
            user         = User.objects.get(id=payload['user_id'])
            request.user = user

        except User.DoesNotExist:
            return JSonResponse({"message": "INVALID_USER"}, status=401)

        except jwt.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=401)

        return func(self, request, *args, **kwargs)

    return wrapper
