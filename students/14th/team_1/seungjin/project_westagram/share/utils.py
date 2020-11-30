import json
import jwt

import my_settings

from django.http import JsonResponse
from django.db.models import Q
from django.utils.decorators import method_decorator

from user.models import (
                        User,
                    )

def getUserIDFromToken(token):    
    user_data   = jwt.decode(token, my_settings.SECRET['secret'], algorithm='HS256')
    return user_data['user_id']

'''
def checkAuthDecorator():
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            data = json.loads(request.body)

            try:
                user_data   = jwt.decode(
                                        data['token'], 
                                        my_settings.SECRET['secret'], 
                                        algorithm='HS256')

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
                return JsonResponse({"message":"You've requested with wrong JSON format."}, 
                                    status=400)

            return func(request, *args, **kwargs)
        return wrapper
    return decorator
'''

def checkAuthDecorator(func):
    def wrapper(self, request, *args, **kwargs):
        data = json.loads(request.body)

        try:
            user_data   = jwt.decode(
                                data['token'], 
                                my_settings.SECRET['secret'], 
                                algorithm='HS256'
                                )

            user_id     = user_data['user_id']

        except Exception:
            return JsonResponse({"message":"[Token] is not allowed."}, status=400)

        if not User.objects.filter(id=user_id).exists():
            return JsonResponse({"message":"User is not exist."}, status=400)
            
        return func(self, request, *args, **kwargs)

    return wrapper

def checkRequestBodyDecorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"message":"You've requested with wrong JSON format."}, 
                                status=400)

        return func(self, request, *args, **kwargs)

    return wrapper



