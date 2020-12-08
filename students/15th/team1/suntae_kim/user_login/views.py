import json
import os
import sys
import bcrypt
import jwt

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

# sys.path.append(
#    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# )

#from suntae_kim.user.models import User
from user.models import User

class UserLogin(View):
    def __init__(self):
        pass
    def post(self, request):
        try:
            data = json.loads(request.body)
            username        = data['username']
            password        = data['password'].encode('utf-8')
            user_info       = User.objects.get(username = username)
            user_id         = user_info.id
            hashed_password = user_info.password.encode('utf-8')

            if bcrypt.checkpw(password, hashed_password):
                SECRET = 'this is my secret'
                access_token = jwt.encode({'id' : user_id}, SECRET, algorithm = 'HS256').decode('utf-8')


                return JsonResponse({'Token' : access_token })

            else:
                return JsonResponse({'MESSAGE' : 'INVALID_USER'})

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'})
