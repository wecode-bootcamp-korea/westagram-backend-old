import json
import os
import sys
import bcrypt
import jwt

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from user.models import User
from user_login.utils import LoginAuthorization

class UserLogin(View):
    def __init__(self):
        pass

    @LoginAuthorization
    def post(self, request):
        try:
            data = json.loads(request.body)
            username        = data['username']
            password        = data['password']

        except ValueError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'})
