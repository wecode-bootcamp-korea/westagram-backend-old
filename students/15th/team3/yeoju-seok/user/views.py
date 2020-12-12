import json
import bcrypt
import jwt

from django.http import JsonResponse
from django.views import View

from user.models import Account
from my_settings import SECRET

class AccountView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            Account.objects.create(
                email = data['email'],
                password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt()).decode()
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
                if password_check == True:
                    access_token = jwt.encode({'id' : user_id},SECRET,algorithm = 'HS256').decode('utf-8')

                    return JsonResponse({"message":"SUCESS", "TOKEN" : access_token},status=200)

                return JsonResponse({"message":"INVALID_PASSWORD"},status=401)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"},status=401)

        except:
            return JsonResponse({"message":"INVALID_USER"},status=401)

