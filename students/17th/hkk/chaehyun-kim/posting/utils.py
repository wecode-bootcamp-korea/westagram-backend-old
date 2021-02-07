import jwt
import json

from django.http    import JsonResponse

from my_settings    import SECRET_KEY, AL
from user.models    import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token    = request.headers['Authorization']
            payload         = jwt.decode(access_token, SECRET_KEY, algorithms=AL)
            user            = User.objects.get(id=payload['user_id'])
            request.user    = user
    # 얘가 안잡혀.... 여기서 말고 posting/views.py 에서 게시글 달기 POST method에서는 잡힘 ㅠㅠ 왜ㅠㅠㅠ
    #    except User.DoesNotExist:
    #        return JsonResponse({'message' : 'INVALID_USER'}, status=400)
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status=400)
        
        return func(self, request, *args, **kwargs)
    
    return wrapper
