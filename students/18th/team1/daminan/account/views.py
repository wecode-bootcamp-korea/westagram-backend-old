import json
import bcrypt
import jwt

from django.views import View
from django.http  import JsonResponse

from .models     import User
from my_settings import SECRET_KEY

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "EMAIL_ERROR"}, status=400)
            if User.objects.filter(password=data['password']).exists():
                return JsonResponse({"message": "PASSOWRD_ERROR"}, status=400)
            if '@' in data['email'] and '.' in data['email'] and len(data['password']) >= 8:
                byted_password = data['password'].encode('utf-8')
                hash_password = bcrypt.hashpw(byted_password, bcrypt.gensalt())
                password = hash_password.decode('utf-8')
                user     = User.objects.create(
                email    = data['email'],
                password = password
            ).save()
                return JsonResponse({"message": "SUCCESS"}, status=200)
            return JsonResponse({"message":"MAKE_FAIL"}, status=400)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
   

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            #if User.objects.filter(email=data['email']).exists():
            user = User.objects.get(email=data['email'])
            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                 
                token = jwt.encode({'email' : data['email']}, SECRET_KEY, algorithm="HS256")
                    #token = token.decode('utf-8')
                    # h5yp 버전 문제로 디코드 안 해도 됨.
                
                return JsonResponse({"message":"SUCCESS"}, status=200)
            else:
                return JsonResponse({"message":"INVALID_USER"}, status=401)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)