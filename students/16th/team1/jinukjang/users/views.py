import json
import re

from django.views import View
from django.http  import JsonResponse

from .models      import User


class SignupView(View):
    def post(self,request):
        try:
            MIN_PASSWORD_LENGHT = 8

            data = json.loads(request.body)

            user_id  = data['user_id']
            password = data['password']
            nickname = data['nickname']
            
            # user, phone, email은 필수가 아님
            name     = data.get('name', None)
            phone    = data.get('phone', None)
            email    = data.get('email', None)
            
            p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            if User.objects.filter(user_id=user_id).exists():
                return JsonResponse({'MESSAGE :':"USER_ID ALREADY EXISTS!"},status = 400)

            if User.objects.filter(nickname=nickname).exists():
                return JsonResponse({'MESSAGE :':"NICKNAME ALREADY EXISTS!"},status = 400)

            if email    != None and p.match(email) == None:
                return JsonResponse({'MESSAGE :':"INVAILD_EMAIL_ADDRESS!"},status = 400)
            
            if email    != None and User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE :':"EMAIL ALREADY EXISTS!"},status = 400)

            if len(password) < MIN_PASSWORD_LENGHT:
                return JsonResponse({'MESSAGE :':"PASSWORD VALIDATION"},status = 400)

            if phone    != None and User.objects.filter(phone=phone).exists():
                return JsonResponse({'MESSAGE :':"PHONE ALREADY EXISTS!"},status = 400)
                    
            print(phone.replace('-','').isdigit())
            if phone    != None and not phone.replace('-','').isdigit():
                return JsonResponse({'MESSAGE :':"PHONENUMBER_SHOULD_CONTAIN_ONLY_DIGITS"},status = 400)
            

            User.objects.create(
                user_id  = user_id,
                nickname = nickname,
                name     = name,
                email    = email,
                phone    = phone,
                password = password
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)
            
        except KeyError:
            return JsonResponse({'MESSAGE': "KEY_ERROR"}, status=400)


class LoginView(View):
    def get(self,request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(user_id=data['user_id'])

            if user.password == data['password']:
                return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)
            return JsonResponse({'MESSAGE': 'WORONG PASSWORD'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)
            
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD USER"},status = 400)
            