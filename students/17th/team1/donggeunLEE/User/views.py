import json
import bcrypt, jwt

from django.http  import HttpResponse, JsonResponse
from django.views import View

from .models      import Userinfo

# 회원가입
MINIMUM_PASSWORD_LENGTH = 8
class UserSignUpView(View):
    #MINIMUM_PASSWORD_LENGTH = 8
    def post(self, request):
        data = json.loads(request.body)
                
        try:
            password_validity = data['password']

            if Userinfo.objects.filter(name = data['name']).exists():
                return JsonResponse({"MESSAGE" : "USER_ALREADY_EXIST"}, status = 400)
        
            if Userinfo.objects.filter(phone_number = data['phone_number']).exists():
                return JsonResponse({"MESSAGE": "INVALID_PHONE_NUMBER"}, status= 400)
        
            if Userinfo.objects.filter(email = data['email']).exists():
                return JsonResponse({"MESSAGE":"INVALID_EMAIL"}, status = 400)
        
            if '@' and '.' not in data['email']:
                return JsonResponse({"MESSAGE" : "Inavailed_KeyError"}, status= 400)
        
            if len(password_validity) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({"MESSAGE" : "SHORT_PASSWORD"}, status= 400)

            Userinfo.objects.create(
                    name         = data['name'],
                    phone_number = data['phone_number'],
                    email        = data['email'],
                    password     = bcrypt.hashpw( data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status = 200)
            
        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)


class UserlonginView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:

            name         = data.get('name', None),
            phone_number = data.get('phone_number', None),
            email        = data.get('email', None),
            password     = bcrypt.hashpw(data.get('password', None).encode('utf-8'), bcrypt.gensalt()).encode('utf-8')
     
            if Userinfo.objects.filter(name=name | Q(email = email) | Q(phone_number = phone_number)).exists():
                user = Userinfo.objects.get(name = name)
                if Userinfo.objects.filter(user.password == password):
                    return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 200)
                else:
                    return JsonResponse({"MESSAGE" : "CHECK_PASSWORD"})
            else:
                return JsonResponse({"MESSAGE" : "INVALID_USER"}, status = 401)
        except KeyError:
            return JsonResponse({"MESSAGE": "SUCCESS"}, status = 401)

