import json
import re

from django.views import View
from django.http import JsonResponse

from user.models import User

class UserView(View):
    def create(self, request):
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


        if email is None and phone is None and name is None:
            return JsonResponse({'MESSAGE': 'KEY_ERRORS'}, status=400)

        if email is not None:
            if not (re.search(email_regex,email)):
                return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=400)

        if password is None:
            return JsonResponse({'MESSAGE': 'KEY_ERRORS'}, status=400)
            
        if not (re.search(password_regex, password)):
            return JsonResponse({'MESSAGE': 'INVALID_PASSWORD'}, status=400)
            
        if name_db.exists() or email_db.exists() or phone_db.exists():
            return JsonResponse({'MESSAGE': 'EXIST_USER'}, status=400)

        User.objects.create(name= name, password= password, email= email, phone= phone)
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)


class LoginView(View):
    def login(self, request):
        data        = json.loads(request.body)
        name        = data.get('name')
        email       = data.get('email')
        phone       = data.get('phone')
        password    = data.get('password')

        if email is None and phone is None and name is None:
            return JsonResponse({'MESSAGE': 'KEY_ERRORS'}, status=400)

        if password is None:
            return JsonResponse({'MESSAGE': 'KEY_ERRORS'}, status=400)

        if name is not None:
            if User.objects.filter(name= name).exists():
                user = User.objects.get(name= name)
                if user.password != password:
                    return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
            else:
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

        if email is not None:
            if User.objects.filter(email= email).exists():
                user = User.objects.get(email= email)
                if user.password != password:
                    return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
            else:
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

        if phone is not None:
            if User.objects.filter(phone= phone).exists():
                user = User.objects.get(phone= phone)
                if user.password != password:
                    return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
            else:
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

        return JsonResponse({"message":"SUCCESS"}, status= 200) 
        