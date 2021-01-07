import jwt
import json

from django.http            import JsonResponse
from westagram.settings     import SECRET
from westagram.my_settings  import ALGORITHM, SECRET

from user.models            import User
from posting.models         import Post

def login_decorator(func):
    def wrapper(request, *args, **kwargs):
        try:
            token        = request.headers.get('authorization')
            payload      = jwt.decode(token, SECRET, algorithms=ALGORITHM) 

            user         = User.object.get(id=payload['user_id'])
            request.user = user
        
        except jwt.DecodeError:
            return JsonResponse({'MESSAGE':'INVALID TOKEN'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': '존재하지 않는 유저입니다'}, status=400)
        
        return func(request, *args, **kwargs)
    return wrapper
        