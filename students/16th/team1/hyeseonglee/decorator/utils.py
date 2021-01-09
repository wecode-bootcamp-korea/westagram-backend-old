import jwt
import json

from django.http            import JsonResponse
from westagram.settings     import SECRET
from westagram.my_settings  import ALGORITHM, SECRET

from user.models            import User
from posting.models         import Post

# def login_decorator(func):
#     print('나와라00000000')

#     def wrapper(self, request, *args, **kwargs):
#         try:
#             token        = request.headers.get('Authorization')
#             print(token,dir(token),'나와라11111111')
            
#             payload      = jwt.decode(token, SECRET, algorithms=ALGORITHM) 
            
#             print(payload,dir(payload),'나와라22222222222')
#             user_id = User.objects.get(id=payload['id'])

#             print(user_id,'나와라33333333333')

#         except jwt.exceptions.DecodeError:
#             return JsonResponse({'MESSAGE':'INVALID TOKEN'}, status=400)
        
#         except User.DoesNotExist:
#             return JsonResponse({'MESSAGE': '존재하지 않는 유저입니다'}, status=400)
        
#         return func(self, request, user_id *args, **kwargs)
#     return wrapper

class LoginConfirm:
    def __init__(self, func):
        self.func = func
        print('-----------------------------------------------------------1번')
    def __call__(self, request, *args, **kwargs):
        print('-----------------------------------------------------------2번')

        token = request.headers.get("Authorization", None)
        try:
            if token:
                payload = jwt.decode(token, SECRET, ALGORITHM)
                request.user = User.objects.get(id = payload['id'])
                return self.func(self, request, *args, **kwargs)
            return JsonResponse({'MESSAGE':'로그인 하세요'}, status=401)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE':'INVALID TOKEN'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': '존재하지 않는 유저입니다'}, status=400)
            