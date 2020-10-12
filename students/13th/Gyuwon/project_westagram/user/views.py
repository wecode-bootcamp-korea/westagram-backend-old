import json
import re
from django.views import View
from django.http  import JsonResponse
from .models      import User

class SignUpView(View):
    def post(self, request):
        data         = json.loads(request.body)
        name         = data['name']
        email        = data['email']
        password     = data['password']
        phone_number = data['phone_number']
            
        # Q 객체
        # how to filter OR condition in django
        if User.objects.filter(Q(email=email) | Q(name=name) | Q(phone_number=phone_number)).exists():
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

            return JsonResponse({"message": "SUCCESS"}, status= 201)
    


def email_validation(email):
    if re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return True
    else:
        return False
