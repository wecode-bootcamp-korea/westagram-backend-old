import json
#import re
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import Accounts


class AccountsView(View):
#필수 정보( 전화번호, 이름, 이메일, 비밀번호)
    def post(self, request):
        data = json.loads(request.body)
        account_db = Accounts.objects.all()
#        try:

        user_name = data['name']
        user_phone_number = data['phone_number']
        user_email = data['email']
        user_password = data['password']
# 이메일 형식 
#            p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
#            if p.match(user_email) != None:
#                Accounts.objects.create(email="user_email")
#            else:
#return JsonResponse({'message':'KEY_ERROR'}, status=400)

# 비밀번호 자리수 å
        if len(user_password) >= 8:
            Accounts.objects.create(password="user_password")
        else:
            return JsonResPonse({'message':'KEY_ERROR1'}, status=400)

                                 # 중복 값 확인:
#        if account_db.filter(user_name = data['user_name']).exists():
#            return JsonResPonse({'message':'KEY_ERROR2'}, status=400)
#
#        if account_db.filter(user_phone_number = data['phone_number']).exists():
#            return JsonResPonse({'message':'KEY_ERROR3'}, status=400)
#
#        if accounts_db.filter(user_email = data['email']).exists():
#            return JsonResPonse({'message':'KEY_ERROR4'}, status=400)

        Accounts.objects.create(name="user_name", phone_number="user_phone_number")
#                                   
#        except KeyError:
 #           return JsonResponse({'message': "KEY_ERROR5"}, status=400)


