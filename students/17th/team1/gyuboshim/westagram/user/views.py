import json
import bcrypt
import jwt

from django.shortcuts   import render
from django.views       import View
from django.http        import HttpResponse, JsonResponse
from django.db.models   import Q

from .models            import User

PASSWORD_LEN_LIMIT = 8

class UserView(View):
    def post(self, request):
        try:
            data            =   json.loads(request.body)
            phone_number    =   data['phone_number']
            email_adress    =   data['email_adress']
            name            =   data['name']
            nickname        =   data['nickname']
            password        =   data['password']
            
            if (email_adress or phone_number) and password:
                
                if User.objects.filter(email_adress = email_adress).exists():
                    return JsonResponse({"message":"EMAIL_ALREADY_EXISTS"}, status = 409)
                
                if User.objects.filter(phone_number = phone_number).exists():
                    return JsonResponse({"message":"PHONENUMBER_ALREADY_EXISTS"}, status = 409)

                if '@' and '.' not in email_adress:
                    return JsonResponse({"message":"NOT_EMAIL"}, status = 400)

                if len(password) < PASSWORD_LEN_LIMIT:
                    return JsonResponse({"message": "SHORT_PASSWORD"}, status = 400)

                User.objects.create(
                                    phone_number    =   phone_number,
                                    email_adress    =   email_adress,
                                    name            =   name,
                                    nickname        =   nickname,
                                    password        =   bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode(),
                                    )
                
                return JsonResponse({"message":"SUCESS"}, status = 200)
            
            else:
                return JsonResponse({"message":"PASSWORD_OR_E-MAIL_DOES_NOT_EXIST"}, status = 401)
        
        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)
    
class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        phone_number    =   data.get('phone_number', None)
        email_adress    =   data.get('email_adress', None)
        nickname        =   data.get('nickname', None)
        password        =   data['password']

        try:
            if User.objects.filter(
                                Q(phone_number  =   phone_number)|
                                Q(email_adress  =   email_adress)|
                                Q(nickname      =   nickname)
                                ).exists():
                user = User.objects.get(
                                Q(phone_number  =   phone_number)|
                                Q(email_adress  =   email_adress)|
                                Q(nickname      =   nickname)
                                )
                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'user':user.id}, 'westagram', algorithm='HS256')
                    return JsonResponse({"message": "LOGIN_SUCESS", 'Token': token}, status = 200)
            else:
                return JsonResponse({"message": "LOGIN_FAIL"}, status = 401)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEYS"}, status = 400)
