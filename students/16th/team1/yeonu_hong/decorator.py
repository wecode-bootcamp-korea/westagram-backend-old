import json
import jwt
from django.http import JsonResponse
from my_settings import SECRET
from user.models import User

# 로그인 체크
def login_check(func):
    def wrapper(self, request, *args, **kwargs):
        data       = json.loads(request.body)
        user_token = jwt.decode(data['token'], SECRET, algorithms='HS256')

        if not User.objects.filter(id=user_token['id']).exists():
            return JsonResponse({'message':'INVALID_USER'}, status=401)
            
        setattr(request, 'user', User.objects.get(id=user_token['id']))
        return func(self, request, *args, **kwargs)
    return wrapper


# 들어오는 키값이 비어있을 경우 체크
