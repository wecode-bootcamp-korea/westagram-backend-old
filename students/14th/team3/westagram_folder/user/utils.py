import jwt
import json

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from .models import Account

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token=request.headers.get('Authorization', None)
            payload=jwt.decode(token, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
            request.user = Account.objects.get(id = payload['user_id'])
            return func(self, request, *args, **kwargs)

        except Account.DoesNotExist:
            return JsonResponse({"message" : "INVALID_USER"}, status=400)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE': 'INVALID TOKEN'}, status=400)
    return wrapper

