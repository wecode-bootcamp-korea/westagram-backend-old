from django.shortcuts import render

import json
from django.views   import View
from django.http    import HttpResponse, JsonResponse

from .models        import User

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


            if user_data['email_adress'] and user_data['password']:
                
                if user_data['email_adress'] == User.objects.filter(email_adress = email_adress):
                    return JsonResponse({'message':'CHANGE_E-MAIL_ADRESS'}, status = 409)
                
                if user_data['phone_number'] == User.objects.filter(phone_number = phone_number):
                    return JsonResponse({'message':'CHANGE_PHONE_NUMBER'}, status = 409)

                if '@' or '.' not in user_data['email_adress']:
                    return JsonResponse({'message':'@_OR_._IS_MISSING_IN_E-MAIL_ADRESS'}, status = 400)

                if len(user_data['password']) < PASSWORD_LEN_LIMIT:
                    return JsonResponse({'message': 'PASSWORD_HAS_TO_BE_AT_LEAST_8-DIGIT'}, status = 400)
                    
                user = User.objects.create(
                                            phone_number    =   user_data['phone_number'],
                                            email_adress    =   user_data['email_adress'],
                                            name            =   user_data['name'],
                                            nickname        =   user_data['nickname'],
                                            password        =   user_data['password']
                                            )
                
                return JsonResponse({'message':'SUCESS'}, status = 200)
            
            else:
                return JsonResponse({'message':'PASSWORD_OR_E-MAIL_IS_MISSING'}, status = 401)
        
        except:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)
    
class LoginView(View):
    def post(self, request):
        data            =   json.loads(request.body)
        phone_number    =   data['phone_number']
        email_adress    =   data['email_adress']
        password        =   data['password']

        if User.objects.filter(
                                phone_number = phone_number,
                                email_adress = email_adress,
                                password = password
                                ).exists():
            return JsonResponse({'message': 'LOGIN SUCESS'}, status = 200)

        else:
            return JsonResponse({'message': 'ID OR PASSWORD DOES NOT MATCH'}, status = 401)
