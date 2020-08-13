import jwt
import json

from django.http import JsonResponse

from .models import User

SECRET_KEY = '=34gct84ha1$^l=owxc&pn*&vi3#f%k@99j2azzfi+2#u^g5ya'

def make_token(id):
    access_token = jwt.encode({'id' : id}, SECRET_KEY, algorithm = 'HS256').decode('utf-8')
    return access_token

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        access_token = request.headers.get('Authorization', None)
        if access_token:
            try:
                header = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')
                user = User.objects.get(id = header['id'])
                request.user = user
            except jwt.DecodeError:
                return JsonResponse({"message" : "EXPIRED_TOKEN"}, status = 401)
            except User.DoesNotExist:
                return JsonResponse({'message' : 'NO_EXISTS_USER'}, status=404)
            return func(self, request, *args, **kwargs)
        return JsonResponse({"message" : "INVALID_USER"}, status = 401)
    return wrapper
        