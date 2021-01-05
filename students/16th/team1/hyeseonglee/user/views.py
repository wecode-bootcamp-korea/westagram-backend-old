import json
import re
from django.http  import JsonResponse
from django.views import View
from django.db.models import Q  

from user.models  import User

class SignUpView(View):

    def post(self, request):
        try:
            data        = json.loads(request.body)
            email       = data['email']
            password    = data['password']
            MIN_LEN_PWD = 8

                    
            p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            if not email and password: 
                return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
            
            if len(password) < MIN_LEN_PWD:  # 유형1
                return JsonResponse({'MESSAGE':f'PASSWORD SHOULD BE OVER {MIN_LEN_PWD} CHAR'}, status=400)
 
            if not p.match(email):
                return JsonResponse({'MESSAGE':'EMAIL ERROR.'}, status=400)
            
            if not User.objects.filter(email=email).exists(): 
                User.objects.create(
                                    password=password,
                                    email   =email                               
                                    )
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
            
            return JsonResponse({'MESSAGE':'EMAIL ALREADY EXISTS.'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR OCCURED!'},status=400)

        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE ERROR OCCURED!'},status=400)
            
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'USER DOES NOT EXISTS'}, status=400)
        

class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
        
            if User.objects.filter(email=email,password=password).exists():
                return JsonResponse({'MESSAGE':'로그인에 성공하셨습니다.'}, status=200)
            return JsonResponse({'MESSAGE':'아이디와 비밀번호에 문제가 있습니다.'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY ERROR OCCURED!'},status=400)

        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE ERROR OCCURED!'},status=400)
