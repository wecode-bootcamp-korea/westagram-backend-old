import jwt

from jwt.exceptions import InvalidSignatureError, DecodeError
from django.http  import JsonResponse

from user.models     import User
from my_settings import SECRET_KEY


def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')

            if not token:
                return JsonResponse({"message": "로그인을 먼저 해주세요."}, status=401)
            
            payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            # {'user_id': 5}

            user_id = payload['user_id']    
            user = User.objects.get(id=user_id)

            request.user = user
        
        # try except 구현하기
        # 1) jwt.exceptions.InvalidSignatureError: Signature verification failed (토큰의 정보가 잘못됨)
        # 2) jwt.exceptions.DecodeError : 토큰에서 header 정보가 잘못됨
            return func(self, request, *args, **kwargs)
        
        except InvalidSignatureError:
            return JsonResponse({"message": "Signature verification failed"})
        
        except DecodeError:
            return JsonResponse({"message": "Invalid header string"})


    return wrapper


