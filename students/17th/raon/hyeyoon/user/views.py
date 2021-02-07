import json

from django                 import views
from django.views           import View
from django.http            import JsonResponse, HttpResponse

from .models import Account

PASSWORD_MIN_LENGTH = 8

class UserSignUpView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            name         = data['name']
            password     = data['password']
            email        = data['email']
            phone_number = data['phone_number']

            if Account.objects.filter(email = email).exists():
                return JsonResponse({"MESSAGE":"INVALID_EMAIL"}, status = 400)

            if Account.objects.filter(name = name).exists():
                return JsonResponse({"MESSAGE":"INVALID_NAME"}, status = 400)

            if Account.objects.filter(phone_number = phone_number).exists():
                return JsonResponse({"MESSAGE":"INVALID_PHONE_NUMBER"}, status = 400)
        
            if len(password) < PASSWORD_MIN_LENGTH:
                return JsonResponse({"MESSAGE":"INVALID_PASSWORD"}, status = 400)
        
            if '@' not in email or '.' not in email:
                return JsonResponse({"MESSAGE":"INVALID_EMAIL"}, status = 400)

            Account.objects.create(
                name         = name,
                password     = password,
                email        = email,
                phone_number = phone_number
            )

            return JsonResponse({"MESSAGE":"SUCCESS"}, status = 200)
        
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)

class UserSignInView(View):
    def post(self,request):
        try:
            data     = json.loads(reaquest.body)
            email    = data['email']
            password = data['password']

            if Account.objects.filter(email = email, password = password).exists():
                return JsonResponse({"message":"SUCCESS"}, status = 200)
            return JsonResponse({"message":"INVALID_USER"}, status = 401)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)




        
