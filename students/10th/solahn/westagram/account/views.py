from django.shortcuts import render

# Create your views here.
import json
from django.views import View
from django.http import JsonResponse
from .models import Account

class SignUpView(View):
   
    
    def post(self, request):
        data = json.loads(request.body)
        if Account.objects.filter(email = data['email']).exists():
            return JsonResponse({'message':'email 중복'}, status=401)
        else:
            Account(
                    email  = data['email'],
                    password = data['password']
                    ).save()
            return JsonResponse({'message': '회원가입 완료'},status=200)

    def get(self, request):
        user_data = Account.objects.values()
        return JsonResponse({'users':list(user_data)},status=200)

    
class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if Account.objects.filter(email = data['email']).exists():
                user = Account.objects.get(email = data['email'])
                if user.password == data['password']:
                    return JsonResponse({'message':f'{user.email}회원님 로그인 성공'}, status=200)
                else:
                    return JsonResponse({'message':'비밀번호 오류'}, status=401)
                return JsonResponse({'message':'INVALID_USER'}, status=400)
           
        except KeyError:
            return JsonResponse({'message':'KeyError'}, status=400)
                


