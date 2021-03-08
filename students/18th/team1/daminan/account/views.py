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
                password = hash_password
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
            user = User.objects.get(email=data['email'])
            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                 
                token = jwt.encode({'email' : data['email']}, SECRET_KEY, algorithm="HS256")
                #라이브러리에서 만들어줌. 이메일 부분 암호화 클라이언트에게 보내줌.(json body에 담아서 보냄)
                #프->백 헤더에 토큰을 담아서 보내줘야 함.
                return JsonResponse({"message":"SUCCESS"}, status=200)
            else:
                return JsonResponse({"message":"INVALID_USER"}, status=401)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        
class TokenCheckView(View):
    def post(self,request):
        data = json.loads(request.body)
        
        user_token_info = jwt.decode(data['token'], SECRET_KEY, algorithms='HS256')
        
        if User.objects.filter(email=user_token_info['email']).exists():
            return JsonResponse({"message": "SUCCESS"}, status=200)
        return JsonResponse({"message":"INVALID_USER"}, status=401)
    
class FollowView(View):
    def post(self,request):
        data   = json.loads(request.body)
        user   = User.objects.get(email=data['email'])
        Follow = Follow.objects.create(
            from_user = user,
            to_user   = user
        )
        return JsonResponse({"message" : "SUCCESS"}, status=200)
        