import json
import re
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Accounts


class AccountsView(View):
#필수 정보( 전화번호, 이름, 이메일, 비밀번호)
    def post(self, request):
        data = json.loads(request.body)
        try:
# 이메일 형식 
            p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if p.match(data['email']) == None:
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

# 비밀번호 자리수 å
            if len(data["password"]) < 8:
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

            # 중복 값 확인:
            if Accounts.objects.all().filter(name = data['name']).exists():
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

            if Accounts.objects.all().filter(phone_number = data['phone_number']).exists():
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

            if Accounts.objects.all().filter(email = data['email']).exists():
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

            Accounts.objects.create(
                    name = data['name'] ,
                    phone_number = data['phone_number'] ,
                    email = data['email'] ,
                    password = data['password'])
            return JsonResponse({'message' : '성공'})

                # Accounts.objects.create(name="user_name", phone_number="user_phone_number")
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR3'}, status=400)

class LoginView(View):
    def post(self, request):
        login_data = json.loads(request.body)
        name = login_data.get('name', None)
        email = login_data.get('email', None)
        password = login_data.get('password', None)
        phone_number = login_data.get('phone_number', None)


        if Accounts.objects.filter(name = name).exists():
            account = Accounts.objects.get(name=name)
            if account.password == password:
                return JsonResponse({'message':'Login SUCCESS'}, status=200)
            return JsonResponse({'message':'wrong account'}, status=401)

        elif Accounts.objects.filter(email = email).exists():
            account = Accounts.objects.get(email=email)
            if account.password == password:
                return JsonResponse({'message':'login success'}, status=200)
            return JsonResponse({'message':'Login Failed - wrong password'}, status=402)

        elif Accounts.objects.filter(phone_number = phone_number).exists():
            account = Accounts.objects.get(phone_number=phone_number)
            if account.password == password:
                return JsonResponse({'message':'login success'}, status=200)
            return JsonResponse({'message':'Login Failed - wrong password'}, status=402)


        return JsonResponse({'message':'Login Failed - wrong account(name or email)'}, status=403)

    def get(self, request):
        pass













