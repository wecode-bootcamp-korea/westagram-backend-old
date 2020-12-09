import json
import os
import sys
import jwt
import bcrypt

from user.models import User
from django.http import JsonResponse

from my_settings import SECRET_KEY

def LoginAuthorization(func):
    def wrapper(self, request):
        try:
            data = json.loads(request.body)

            username = data['username']
            password = data['password'].encode('utf-8')

            user_info = User.objects.get( username = username )
            user_id = user_info.id
            user_password = user_info.password
#            hashed_password = user_info.password.encode('utf-8')
            hashed_password = user_password.encode('utf-8')

            if bcrypt.checkpw(password, hashed_password):
                access_token = jwt.encode({'id' : user_id}, SECRET_KEY, algorithm = 'HS256').decode('utf-8')
                return JsonResponse({'MESSAGE' : hashed_password.decode('utf-8')})
            else:
                return JsonResponse({'MESSAGE' : 'ERROR'})
        except:
            return JsonResponse({'MESSAGE' : 'INVALID_USER'})
        return func(self, request)
    return wrapper
