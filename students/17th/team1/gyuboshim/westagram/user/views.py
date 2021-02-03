from django.shortcuts   import render
from django.views       import View
from django.http        import HttpResponse, JsonResponse
from django.db.models   import Q

from .models            import User

import json

PASSWORD_LEN_LIMIT = 8

class UserView(View):
    def post(self, request):
        try:
            data            =   json.loads(request.body)
            user_data       =   data['user']
            phone_number    =   user_data['phone_number']
            email_adress    =   user_data['email_adress']
            name            =   user_data['name']
            nickname        =   user_data['nickname']
            password        =   user_data['password']

            if (email_adress or phone_number) and password:
                
                if User.objects.filter(email_adress = email_adress).exists():
                    return JsonResponse({"message":"EMAIL_ALREADY_EXISTS"}, status = 409)
                
                if User.objects.filter(phone_number = phone_number).exists():
                    return JsonResponse({"message":"PHONENUMBER_ALREADY_EXISTS"}, status = 409)

                if '@' or '.' not in email_adress:
                    return JsonResponse({"message":"@_OR_._DOES_NOT_EXIST"}, status = 400)

                if len(password) < PASSWORD_LEN_LIMIT:
                    return JsonResponse({"message": "PASSWORD_HAS_TO_BE_AT_LEAST_8-DIGIT"}, status = 400)
                    
                user = User.objects.create(
                                            phone_number    =   phone_number,
                                            email_adress    =   email_adress,
                                            name            =   name,
                                            nickname        =   nickname,
                                            password        =   password
                                            )
                
                return JsonResponse({"message":"SUCESS"}, status = 200)
            
            else:
                return JsonResponse({"message":"PASSWORD_OR_E-MAIL_DOES_NOT_EXIST"}, status = 401)
        
        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"}, status = 400)
    
class LoginView(View):
    def post(self, request):
        data            =   json.loads(request.body)
        user_data       =   data['user']
        phone_number    =   user_data['phone_number']
        email_adress    =   user_data['email_adress']
        name            =   user_data['name']
        password        =   user_data['password']

        if User.objects.filter(
                                Q(phone_number  =   phone_number)|
                                Q(email_adress  =   email_adress)|
                                Q(name          =   name)
                                ).exists():
            user = User.objects.get(
                                Q(phone_number  =   phone_number)|
                                Q(email_adress  =   email_adress)|
                                Q(name          =   name)
                                )
            if user['password'] == password:
                return JsonResponse({"message": "LOGIN_SUCESS"}, status = 200)

        else:
            return JsonResponse({"message": "ID_OR_PASSWORD_DOES_NOT_MATCH"}, status = 401)
