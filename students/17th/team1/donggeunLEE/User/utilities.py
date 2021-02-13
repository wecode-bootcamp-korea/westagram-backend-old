import json
import jwt
import requests

from django.http import HttpResponse, JsonResponse
from django.conf import settings

from .models     import Userinfo
import my_settings


def login_decorator(func):
    def wrapper(self, request, *arg, **kwargs):
        try:
            access_token = request.headers['Authorization']
            payload = jwt.decode(access_token, 'secret', algorithm='HS265')
            user  = Userinfo.objects.get(id = payload['id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({"MESSAGE" : "INAVLIED_TOKEN"}, status= 400)

        except Userinfo.DoesNotExist:
            return JsonResponse({"MESSAGE":"INVALIED_USER"}, status=400)
        return func(self, request, *arg, **kwargs)
    
    return wrapper




