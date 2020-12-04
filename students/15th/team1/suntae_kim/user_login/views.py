import json
import os
import sys

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
            username = data['username']
            password = data['password']

            if not User.objects.filter(username = username, password = password):
                return JsonResponse({'MESSAGE' : 'INVALID_USER'})
            else:
                return JsonResponse({'MESSAGE' : 'SUCCESS'})
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'})
