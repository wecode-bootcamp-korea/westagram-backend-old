import json
import jwt

from django.http import HttpResponse, JsonResponse
from django.conf import settings

from .models     import Userinfo



def login_decorator(func):
    def wrapper(self, request, *arg, **kwargs):
        try:
            access_token = request.headers['Authorization']
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms='HS256')
            user  = Userinfo.objects.get(id=payload['id'])
            request.user = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({"MESSAGE" : "INAVLIED_TOKEN"}, status= 400)

        except Userinfo.DoesNotExist:
            return JsonResponse({"MESSAGE":"INVALIED_USER"}, status=400)
        return func(self, request, *arg, **kwargs)
    return werapper




