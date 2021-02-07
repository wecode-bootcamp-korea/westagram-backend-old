import json
import bcrypt
import jwt

from django                 import views
from django.views           import View
from django.http            import JsonResponse, HttpResponse

from .models import Account

PASSWORD_MIN_LENGTH = 8

class UserSignUpView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            name            = data['name']
            password        = data['password']
            email           = data['email']
            phone_number    = data['phone_number']

            if Account.objects.filter(email = email).exists():
                return JsonResponse({"MESSAGE":"INVALID_EMAIL"}, status = 400)

            if Account.objects.filter(name = name).exists():
                return JsonResponse({"MESSAGE":"INVALID_NAME"}, status = 400)

            if Account.objects.filter(phone_number = phone_number).exists():
                return JsonResponse({"MESSAGE":"INVALID_PHONE_NUMBER"}, status = 400)
        
            if len(data['password']) < PASSWORD_MIN_LENGTH:
                return JsonResponse({"MESSAGE":"INVALID_PASSWORD"}, status = 400)
        
            if '@' not in email or '.' not in email:
                return JsonResponse({"MESSAGE":"INVALID_EMAIL"}, status = 400)

            Account.objects.create(
                name         = name,
                password     = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8'),
                email        = email,
                phone_number = phone_number
            )

            return JsonResponse({"MESSAGE":"SUCCESS"}, status = 200)
        
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)

class UserSignInView(View):
    def post(self,request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if Account.objects.filter(email = email).exists():
                user = Account.objects.get(email = email)

                if bcrypt.checkpw(password.encode('utf-8'),user.password.encode('utf-8')):
                    token = jwt.encode({'user':user.id}, 'secret', algorithm = 'HS256')
                    return JsonResponse({"TOKEN": token, "MESSAGE":"SUCCESS"}, status = 200)
                return JsonResponse({"MESSAGE":"INVALID_PASSWORD"}, status = 401)
            return JsonResponse({"MESSAGE":"INVALID_USER"}, status = 401)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status = 400)




        
