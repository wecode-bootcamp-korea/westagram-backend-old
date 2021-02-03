import json

from django.views     import View
from django.http      import HttpResponse, JsonResponse
from django.db.models import Q

from .models      import Account

class SignupView(View):
    def post(self, request):
        signup_data = json.loads(request.body)

        try:
            if Account.objects.filter(email=signup_data['email']).exists() or Account.objects.filter(phonenumber=signup_data['phonenumber']).exists() or Account.objects.filter(name=signup_data['name']).exists():                  

                return JsonResponse({"message":"EXIST_USER"}, status=400) #에러메세지에도 컨벤션이있나요?
            if len('password') < 8:
                return JsonResponse({"message":"PWD must be over 8 digits"}, status=400)
            if '@' or '.' not in email:
                return JsonResponse({"message":"Email must include @ or ."}, status=400) 
             
            Account.objects.create(
                    email       = signup_data['email'],
                    password    = signup_data['password'],
                    nickname    = signup_data['nickname'],
                    name        = signup_data['name'],
                    phonenumber = signup_data['phonenumber'],
            
            )

            return JsonResponse({"message":"SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

            


# Create your views here.
