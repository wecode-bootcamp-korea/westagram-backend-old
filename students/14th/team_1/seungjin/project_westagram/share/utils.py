import json
import jwt
import my_settings
from django.http import JsonResponse
from django.db.models import Q
from user.models import (
                        Users,
                    )
from django.utils.decorators import method_decorator

'''
def getUserID(user_input):
    q = Users.objects.filter(
                    Q(name          = user_input)|
                    Q(phone_number  = user_input)|
                    Q(email         = user_input)
                    )

    if q.exists():
        return q[0].id
    else:
        return None
'''

def getUserIDFromToken(token):    
    user_data   = jwt.decode(token, my_settings.SECRET['secret'], algorithm='HS256')
    return user_data['user_id']
   
'''
def checkAuthorization(token):
    try:
        user_data   = jwt.decode(token, my_settings.SECRET['secret'], algorithm='HS256')
        user_id     = user_data['user_id']
    except jwt.InvalidSignatureError:
        return None

    if Users.objects.filter(id=user_id).exists():
        return user_id
    else:
        return None


def checkRequestBody(request):
    try:
        data    = json.loads(request.body)
        return None
    except Exception as ex:
        return JsonResponse({"message":"You've requested with wrong JSON format."}, status=400)
'''

def checkAuthDecorator():
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            data = json.loads(request.body)
            try:
                user_data   = jwt.decode(data['token'], my_settings.SECRET['secret'], algorithm='HS256')
                user_id     = user_data['user_id']
            except Exception:
                return JsonResponse({"message":"[Token] is not allowed."}, status=400)

            if not Users.objects.filter(id=user_id).exists():
                return JsonResponse({"message":"User is not exist."}, status=400)
            
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

def checkRequestBodyDecorator():
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            try:
                json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"message":"You've requested with wrong JSON format."}, status=400)

            return func(request, *args, **kwargs)
        return wrapper
    return decorator
