from django.views import View 
from .models import Users
from django.http import JsonResponse
import json
# Create your views here.
class Sign_Up(View):
    def post(self, request):
        request = json.loads(request.body)
        LEN_PASSWORD = 8
    
        phone_number = request['phone_number']
        user_name    = request['user_name']
        email        = request['email']
        password     = request['password']
   
        if not phone_number and user_name or not email:
            return JsonResponse({"message" :"KEY_ERROR"}, status = 400)

        elif Users.objects.filter(user_name = user_name, phone_number = phone_number).exists() == True or Users.objects.filter(email = email).exists() == True:
            return JsonResponse({"message" :"이미 회원가입이 되어 있습니다."}, status = 400)

        elif not password:
                return JsonResponse({"message" :"KEY_ERROR"}, status = 400)
        elif int(password) < LEN_PASSWORD:
                return JsonResponse({"message" :"비밀번호를 8자리 이상 입력해주세요."}, status = 400)

        else:
            Users.objects.create(phone_number = phone_number,
                             user_name    = user_name,
                             email        = email,
                             password     = password
                             )
            return JsonResponse({"message" :"SUCCESS"}, status = 200)

         
        
        
        
