import json
import re

from django.views import View
from django.http  import JsonResponse, request

from user.models import User

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email         = data['email']
            phone         = data.get('phone', None)
            full_name     = data.get('full_name', None)
            user_name     = data.get('user_name', None)
            password      = data['password']
            date_of_birth = data.get('date_of_birth', None)

            if phone:
                phone = phone.replace('-','')

            if re.search('@', email) == None or re.search('\.', email) == None:
                return JsonResponse({'message':'EMAIL VALIDATION ERROR'}, status=400)
            if re.search('\S{8,20}', password) == None:
                return JsonResponse({'message':'PASSWORD VALIDATION ERROR'}, status=400)

            if not User.objects.filter(email=email):
                if phone and User.objects.filter(phone=phone):
                    return JsonResponse({'message':'PHONE ALREADY EXISTS'}, status=400)
                elif user_name and User.objects.filter(user_name=user_name):
                    return JsonResponse({'message':'USER_NAME ALREADY EXISTS'}, status=400)
            else:
                return JsonResponse({'message':'EMAIL ALREADY EXISTS'}, status=400)

            User.objects.create(
                email         = email,
                phone         = phone,
                full_name     = full_name,
                user_name     = user_name,
                password      = password,
                date_of_birth = date_of_birth,
            )
            return JsonResponse({'message':'SUCCESS'}, status=200)            
        except KeyError:
            return JsonResponse({'message':'KEY ERROR'}, status=400)
        except:
            return JsonResponse({"message":"RESPONSE ERROR"}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user_name = data['user_name']
            password  = data['password']

            if not User.objects.get(user_name=user_name) and not User.objects.get(email=user_name) and not User.objects.get(phone=user_name):
                return JsonResponse({"message":"INVALID_USER"}, status=401)
            else:
                if not User.objects.get(password=password):
                    return JsonResponse({"message":"INVALID_USER"}, status=401)

            return JsonResponse({"message":"SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        except:
            return JsonResponse({"message":"RESPONSE_ERROR"}, status=400)