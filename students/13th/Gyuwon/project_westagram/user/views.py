import json
import re
from django.db.models import Q
from django.views     import View
from django.http      import JsonResponse
from .models          import User


class SignUpView(View):
    def post(self, request):
        data         = json.loads(request.body)
        name         = data['name']
        email        = data['email']
        password     = data['password']
        phone_number = data['phone_number']
            
        if User.objects.filter(Q(email=data['email']) | Q(name=data['name']) | Q(phone_number=data['phone_number'])).exists():
            return JsonResponse({"message": "Existing user."}, status=409)

        elif email_validation(email) == False:
            return JsonResponse({"message":"Email is not valid."}, status=400)
                        
        elif len(password) <= 7:
            return JsonResponse({"message":"Password is not valid."}, status=400)

        elif email == '' or password == '':
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
            
        else:
            User.objects.create(
                    email        = data['email'],
                    name         = data['name'],
                    password     = data['password'],
                    phone_number = data['phone_number']
                    )

            return JsonResponse({"message": "SUCCESS!"}, status= 201)
    
def email_validation(email):
    if re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return True
    else:
        return False

class SignInView(View):
    def post(self, request):
        data         = json.loads(request.body)
        name         = data['name']
        email        = data['email']
        password     = data['password']
        phone_number = data['phone_number']

        try:
            if email == '' or name == '' or phone_number == '' or password =='':
                return JsonResponse({"message": "KEY_ERROR"}, status=400)
            elif User.objects.get(Q(email=data['email']) | Q(name=data['name'] | Q(phone_number=data['phone_number'])) , password=data['password']):
                return JsonResponse({"message": "SUCCESS"}, status=200)
        except:
            return JsonResponse({"message": "INVALID_USER"}, status=401)