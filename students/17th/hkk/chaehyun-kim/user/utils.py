import jwt
import json

from django.http    import JsonResponse
from my_settings    import SECRET_KEY
from user.models    import User

def LoginAuthorization(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token    = request.headers['Authorization']
            payload         = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')
            user            = User.objects.get(id=payload['user'])
            request.user    = user

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status=400)
        
        except :
            return JsonResponse({'message' : 'INVALID_USER'}, status=400)
        return func(self, request, *args, **kwargs)

    return wrapper
