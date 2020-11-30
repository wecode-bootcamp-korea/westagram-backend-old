from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Accounts
import json
import re


class AccountsView(View):
#필수 정보( 전화번호, 이름, 이메일, 비밀번호)
    def post(self, request):
        data = json.loads(request.body)
        try:
# 이메일 형식 
            p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if not p.match(data['email']):
                return JsonResponse({'message':'이메일 오류'}, status=400)

# 비밀번호 자리수 å
            if len(data["password"]) < 8:
                return JsonResponse({'message':'패스워드 오류'}, status=400)

            # 중복 값 확인:
            if Accounts.objects.filter(name = data['name']).exists():
                return JsonResponse({'message':'존재하는 이름입니다.'}, status=400)

            if Accounts.objects.filter(phone_number = data['phone_number']).exists():
                return JsonResponse({'message':'존재하는 휴대폰 번호입니다.'}, status=400)

            if Accounts.objects.filter(email = data['email']).exists():
                return JsonResponse({'message':'존재하는 이메일입니다.'}, status=400)

            Accounts.objects.create(
                    name         = data['name'] ,
                    phone_number = data['phone_number'] ,
                    email        = data['email'] ,
                    password     = data['password'])
            return JsonResponse({'message' : '성공'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR3'}, status=400)

class LoginView(View):
    def post(self, request):
        try:

            login_data   = json.loads(request.body)
            name         = login_data['name']
            email        = login_data['email']
            password     = login_data['password']
            phone_number = login_data['phone_number']

            if Accounts.objects.filter(name = name).exists():
                account = Accounts.objects.get(name=name)
                if account.password == password:
                    return JsonResponse({'message':'Login SUCCESS'}, status=200)
                return JsonResponse({'message':'Login Failed - wrong password'}, status=401)

            if Accounts.objects.filter(email = email).exists():
                account = Accounts.objects.get(email=email)
                if account.password == password:
                    return JsonResponse({'message':'login success'}, status=200)
                return JsonResponse({'message':'Login Failed - wrong password'}, status=401)

            if Accounts.objects.filter(phone_number = phone_number).exists():
                account = Accounts.objects.get(phone_number=phone_number)
                if account.password == password:
                    return JsonResponse({'message':'login success'}, status=200)
                return JsonResponse({'message':'Login Failed - wrong password'}, status=401)

        except:
            return JsonResponse({'message':'Login Failed - wrong account(name or email or phone_number)'}, status=401)












