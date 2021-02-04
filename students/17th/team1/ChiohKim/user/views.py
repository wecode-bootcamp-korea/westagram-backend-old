import json

from django.views     import View
from django.http      import HttpResponse, JsonResponse
from django.db.models import Q

from .models      import Account

class SignupView(View):
    def post(self, request):
        signup_data = json.loads(request.body)
        MINIMUM_PASSWORD_LENGTH = 8

        try:
            if Account.objects.filter(Q(email=signup_data['email']) | Q(phonenumber=signup_data['phonenumber'])|Q(nickname=signup_data['nickname'])):
                return JsonResponse({"message":"EXIST_USER"}, status=400) 
            if len('password') < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({"message":"INVALID_PASSWORD"}, status=400)
            if '@' or '.' not in email:
                return JsonResponse({"message":"INVALID_EMAIL"}, status=400) 
             
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

            
