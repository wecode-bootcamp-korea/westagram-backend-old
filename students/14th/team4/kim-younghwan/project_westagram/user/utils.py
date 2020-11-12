import jwt
import json
import requests

from django.http                    import JsonResponse
from django.core.exceptions         import ObjectDoesNotExist

from project_westagram.settings     import SECRET_KEY, ABC
from user.models                    import Accounts

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization',None) 
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=ABC)
            user = Accounts.objects.get(id=payload['id'])
            request.user = user
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=400)
        
        except Accounts.DoesNotExist:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=400)
        
        return func(self, request, *args, **kwargs)
    
    return wrapper