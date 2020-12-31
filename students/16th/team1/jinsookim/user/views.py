import json
import bcrypt
from django.views import View 
from .models import Users
from django.http import JsonResponse
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
        q = Q()
        try:
            account  = data['account']
            new_password = data['password']

            if Users.objects.filter(Q(user_name=account) | Q(phone_number=account) | Q(email =account)).exists() == True and Users.objects.filter(password=bcrypt.checkpw(new_password.encode('utf-8'),password)).exists() == True:
                return JsonResponse( {"message": "SUCCESS"}, status = 200)

            return JsonResponse({"message": "INVALID_USER"}, status = 401) 
            
        except KeyError as e:
            return JsonResponse({"message" : e.args[0]}, status = 400)


def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = data['user']

        if Users.objects.filter(email = user).exists() == False:
            return JsonResponse({'message' : '알 수 없는 사용자입니다.'}, status=401)

        return func(self, request, *args, **kwargs)

    return wrapper