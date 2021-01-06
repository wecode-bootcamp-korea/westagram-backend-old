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

            request.headers.b = '1123'
            print('시작')
            print('request.headers.b : ',request.headers.b)
            print()
            print('DIR로 뜯어보기',dir(request.headers))
            print()
            print('request.headers의 데이터 유형',type(request.headers))
            print()
            token        = request.headers.get('b','hello')
            print(token,'=======================')
            payload      = jwt.decode(token, SECRET, algorithms=ALGORITHM) 
            # print(payload,'=====================')
            user         = User.object.get(id=payload['user_id'])
            request.user = user
        
        except jwt.DecodeError:
            return JsonResponse({'MESSAGE':'INVALID TOKEN'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': '존재하지 않는 유저입니다'}, status=400)
        
        return func(request, *args, **kwargs)
    return wrapper
        