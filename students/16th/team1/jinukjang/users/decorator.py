import jwt
import json
from django.http import JsonResponse
from westagram.settings import SECRET

from users.models import User
from posts.models import Post

from my_settings  import ALGORITHM, SECRET


def login_decorator(func): 
    def wrapper(self, request, *args, **kwargs):

        try:
            token        = request.headers.get('Authorization')
            payload      = jwt.decode(token, SECRET, algorithms=ALGORITHM)
            user         = User.objects.get(id=payload['user_id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'},status=400)

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'},status=400)

        return func(self, request, *args, **kwargs)
    return wrapper