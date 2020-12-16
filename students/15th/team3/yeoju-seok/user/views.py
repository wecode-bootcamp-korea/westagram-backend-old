import json, bcrypt, jwt, re

from django.http import JsonResponse
from django.views import View

from user.models import Account
from my_settings import SECRET,ALGORITHM

class AccountView(View):
    def post(self, request):
        data = json.loads(request.body)
        REGAX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        REGEX_PASSWORD = '^[A-Za-z0-9@#$%^&+=]{8,}$'

        try:
            if not re.match(email_validation, data['email']):
                return JsonResponse(
                    {"message":"INVALID_MAIL"},status=401
                )

            if not re.match(pw_validation, data['password']):
                return JsonResponse(
                    {"message":"INVALID_PW"},status=401
                )
            if Account.objects.filter(email=data['email']).exists():
                return JsonResponse(
                    {"message":"USER_EXIST"},status=400
                )

            else:
                Account.objects.create(
                        email = data['email'],
                        password  = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt()).decode()
                )
                return JsonResponse({"message":"SUCCESS"},status=200)

        except:
            return JsonResponse({"message":"KEY_ERROR"},status=401)

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        user_pw = Account.objects.get(email=data['email']).password
        user_id = Account.objects.get(email=data['email']).id
        password_check = bcrypt.checkpw(data['password'].encode('utf-8'),user_pw.encode('utf-8'))

        try:
            if Account.objects.all().filter(email=data['email']).exists():
                if bcrypt.checkpw(data['password'].encode('utf-8').user_pw.encode('utf-8')):
                    access_token = jwt.encode({'id' : user_id},SECRET,ALGORITHM).decode('utf-8')

                    return JsonResponse({"message":"SUCCESS", "TOKEN" : access_token},status=200)

                return JsonResponse({"message":"INVALID_PASSWORD"},status=402)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=401)

        except ValueError:
            return JsonResponse({"message":"INVALID_USER"},status=401)

