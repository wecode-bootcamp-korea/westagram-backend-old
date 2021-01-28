import bcrypt
import jwt
import json
import re

from django.views import View
from django.http  import JsonResponse

from .models      import User, Follow
from my_settings  import SECRET, ALGORITHM
from .decorator   import login_decorator


class SignupView(View):
    def post(self,request):
        try:
            MIN_PASSWORD_LENGHT = 8

            data = json.loads(request.body)

            password = data['password']
            
            # user, phone, email은 필수가 아님
            name  = data.get('name')
            phone = data.get('phone')
            email = data.get('email')
            
            p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            if email and p.match(email) == None:
                return JsonResponse({'MESSAGE':"INVAILD_EMAIL_ADDRESS!"},status = 400)
            
            if email and User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE':"EMAIL ALREADY EXISTS!"},status = 400)

            if len(password) < MIN_PASSWORD_LENGHT:
                return JsonResponse({'MESSAGE':"PASSWORD VALIDATION"},status = 400)

            if phone and User.objects.filter(phone=phone).exists():
                return JsonResponse({'MESSAGE':"PHONE ALREADY EXISTS!"},status = 400)
                    
            if phone and not phone.replace('-','').isdigit():
                return JsonResponse({'MESSAGE' : "PHONENUMBER_SHOULD_CONTAIN_ONLY_DIGITS"},status = 400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            User.objects.create(
                name     = name,
                email    = email,
                phone    = phone,
                password = hashed_password.decode('utf-8') # 데이터베이스 컬럼의 형식이 문자열만 받기 때문에 다시 decode
            )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
            
        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"}, status=400)


class LoginView(View):
    def post(self,request):
        try:
            data     = json.loads(request.body)
            user     = User.objects.get(email=data['email'])
            password = data['password']

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                user_token = jwt.encode({'user_id': user.id}, SECRET, algorithm=ALGORITHM)
                return JsonResponse({'Authorization':user_token}, status=200)
            return JsonResponse({'MESSAGE':'WORONG PASSWORD'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"},status = 400)
            
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVALID USER"},status = 400)
            

class FollowView(View):
    @login_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            to_user = User.objects.get(email=data['to_email'])
            follow  = Follow.objects.filter(to_user=to_user, from_user=request.user)

            if  follow:
                follow.delete()
                return JsonResponse({'MESSAGE':"REMOVE FOLLOW"},status = 200)

            Follow.objects.create(to_user=to_user, from_user=request.user)
            return JsonResponse({'MESSAGE':"SUCESS FOLLOW"},status = 200)
            
        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"},status = 400)
            
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':"INVALID USER"},status = 400)
        