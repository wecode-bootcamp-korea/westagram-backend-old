import json
import bcrypt
from django.views import View 
from .models import Users
from django.http import JsonResponse
from user.utils import login_decorator
from django.db.models import Q



# Create your views here.
class Sign_Up(View):
    def post(self, request):
        data         = json.loads(request.body)
        LEN_PASSWORD = 8
        try:
            phone_number = data['phone_number']
            user_name    = data['user_name']
            email        = data['email']
            password     = data['password']
            if data['email'] not in "@" or data['email'] not in '.':
                return JsonResponse({"message" :"이메일 형식을 지켜주세요"}, status = 400)
                
            if Users.objects.filter(user_name = user_name, phone_number = phone_number).exists() == True or Users.objects.filter(email = email).exists() == True:
                return JsonResponse({"message" :"이미 회원가입이 되어 있습니다."}, status = 400)

            elif len(password) < LEN_PASSWORD:
                return JsonResponse({"message" :"비밀번호를 8자리 이상 입력해주세요."}, status = 400)

            Users.objects.create(phone_number = phone_number,
                                user_name     = user_name,
                                email         = email,
                                password      = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                                )
            return JsonResponse({"message" :"SUCCESS"}, status = 200)

        except KeyError as e:
            return JsonResponse({"message" : e.args[0]}, status = 400)

        
        
class Sign_in(View):
    def post(self, request):
        data  = json.loads(request.body)
        try:
            account  = data['account']
            new_password = data['password']

            if Users.objects.filter(Q(user_name=account) | Q(phone_number=account)|Q(email =account)).exists()==True and Users.objects.filter(password=bcrypt.checkpw(new_password.encode('utf-8'),password)).exists() == True:
                return JsonResponse( {"message": "SUCCESS"}, status = 200)

            return JsonResponse({"message": "INVALID_USER"}, status = 401) 

        except KeyError as e:
            return JsonResponse({"message" : e.args[0]}, status = 400)
            
        
            
