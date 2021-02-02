import json
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import re

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

import bcrypt
import jwt

from .models     import Accounts
import my_settings

MINIMUM_PASSWORD_LEN = 8
EMAIL_VALIDATION     = re.compile('[0-9a-zA-Z_-]+[@]{1}[a-zA-Z]+[.]{1}[a-zA-Z]+') 

class AccountView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        # 필수사항 미입력시
        try:
            email        = data['email']
            password     = data['password']
            name         = data['name']
            nickname     = data['nickname']
            phone_number = data['phone_number']

            # email, password check
            if not EMAIL_VALIDATION.match(email):
                return JsonResponse({'message': 'EMAIL_VALIDATION'}, status=400)
            if len(password) < MINIMUM_PASSWORD_LEN:
                return JsonResponse({'message': 'PASSWORD_VALIDATION'}, status=400)
            else:
                password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # duplicate check
            if Accounts.objects.filter(nickname=nickname) or Accounts.objects.filter(email=email) or Accounts.objects.filter(phone_number=phone_number):
                return JsonResponse({'message': 'DATA_DUPLICATE'}, status=400)
            
            Accounts.objects.create(
                email        = email,
                name         = name,
                nickname     = nickname,
                password     = password,
                phone_number = phone_number
            )

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        access_token = data.get('token')

        if access_token:
            payload = jwt.decode(access_token, my_settings.SECRET, algorithms=my_settings.ALGORITHM)
            if Accounts.objects.filter(email=payload['email']):
                # print('-------------------------- token!!')
                return JsonResponse({'message': 'SUCCESS', 'token': access_token, 'info': payload}, status=200)

        try:
            email        = data.get('email')
            nickname     = data.get('nickname')
            phone_number = data.get('phone_number')
            password     = data['password']

            # password, login_id check
            account = Accounts.objects.get(Q(email=email) | Q(nickname=nickname) | Q(phone_number=phone_number))

            # if email:
            #     account = Accounts.objects.get(email=email)
            # if nickname:
            #     account = Accounts.objects.get(nickname=nickname)
            # if phone_number:
            #     account = Accounts.objects.get(phone_number=phone_number)

            if not bcrypt.checkpw(password.encode('utf-8'), account.password):
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
            
            access_token = jwt.encode({'email' : account.email}, my_settings.SECRET, algorithm=my_settings.ALGORITHM)

            return JsonResponse({'message': 'SUCCESS', 'token': access_token}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)