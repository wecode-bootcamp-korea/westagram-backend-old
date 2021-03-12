import jwt
import json

from django.http import JsonResponse

from .models import User
from my_settings import SECRET_KEY, ALGORITHM

def signin_required(func):
    def wrapper(self,request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)

        if access_token:
            try:
                payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
                signin_user = User.objects.get(id=payload['user_id'])
                
                request.user = signin_user
            except jwt.DecodeError:
                return JsonResponse({'message':'wrong token'}, status=400)
            except User.DoesNotExist:
                return JsonResponse({'message':'존재하지 않는 id'}, status = 401)
            return func(self,request, *args, **kwargs)
        return JsonResponse({'message':'로그인필요'}, status = 401)
    return wrapper
