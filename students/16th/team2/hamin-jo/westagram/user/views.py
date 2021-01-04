import json
import re

from django.views import View
from django.http import JsonResponse

from user.models import User

class UserView(View):
    def post(self, request):
        data           = json.loads(request.body)
        name           = data.get('name')
        password       = data.get('password')
        email          = data.get('email')
        phone          = data.get('phone')
        email_regex    = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        password_regex = '[A-Za-z0-9@#$]{8,12}'
        name_db        = User.objects.filter(name=name)
        email_db       = User.objects.filter(email=email)
        phone_db       = User.objects.filter(phone=phone)

        # email, phone, name 중 1개이상 입력 확인
        if not email and not phone and not name:
            return JsonResponse({'MESSAGE': 'KEY_ERRORS'}, status=400)
        
        # password 입력확인
        if not password:
            return JsonResponse({'MESSAGE': 'KEY_ERRORS'}, status=400)

        # password 조건확인
        if not (re.search(password_regex, password)):
            return JsonResponse({'MESSAGE': 'INVALID_PASSWORD'}, status=400)

        # email 입력시, 조건확인과 기존회원 유무확인
        if email:
            if not (re.search(email_regex,email)):
                return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=400)
            if email_db.exist():
                return JsonResponse({'MESSAGE': 'EXIST_USER'}, status=400) 

        # name 입력시 기존회원 유무확인
        if name:
           if name_db.exists():
               return JsonResponse({'MESSAGE': 'EXIST_USER'}, status=400)
        
        # phone 입력시 기존회원 유무확인
        if phone:
            if phone_db.exists():
                return JsonResponse({'MESSAGE': 'EXIST_USER'}, status=400)
                
        User.objects.create(name= name, password= password, email= email, phone= phone)
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)


class LoginView(View):
    def post(self, request):
        data        = json.loads(request.body)
        name        = data.get('name')
        email       = data.get('email')
        phone       = data.get('phone')
        password    = data.get('password')

        # email, phone, name 중 1개이상 입력 확인
        if not email and not phone and not name:
            return JsonResponse({'MESSAGE': 'KEY_ERRORS'}, status=400)

        # password 입력확인
        if not password:
            return JsonResponse({'MESSAGE': 'KEY_ERRORS'}, status=400)

        # name 입력 시 회원 유무 확인 후 password 매칭 확인
        if not name:
            if User.objects.filter(name= name).exists():
                user = User.objects.get(name= name)
                if user.password != password:
                    return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
            else:
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

        # email 입력 시 회원 유무 확인 후 password 매칭 확인
        if not email:
            if User.objects.filter(email= email).exists():
                user = User.objects.get(email= email)
                if user.password != password:
                    return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
            else:
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

        # phone 입력 시 회원 유무 확인 후 password 매칭 확인
        if not phone:
            if User.objects.filter(phone= phone).exists():
                user = User.objects.get(phone= phone)
                if user.password != password:
                    return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
            else:
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
        
        return JsonResponse({"message":"SUCCESS"}, status= 200) 
        