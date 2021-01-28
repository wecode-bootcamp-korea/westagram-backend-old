import json
import re
import bcrypt
import jwt

from django.http   import JsonResponse
from django.views  import View

from user.models   import User
from my_settings   import SECRET_KEY, ALGORITHM

class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)

        # email 정규표현식
        vali_email = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        validate_email=re.compile(vali_email)

        try:
            if not data['email']:
                return JsonResponse(
                    {'MESSAGE' : 'email을 입력해주세요'}, status = 400)
            
            if not validate_email.match(data['email']):
                return JsonResponse(
                    {'MESSAGE' : '잘못된 email형식'}, status = 400)

            if len(data['password']) < 8 :
                return JsonResponse(
                    {'MESSAGE' : 'password는 8자리 이상'}, status = 400)

            if (User.objects.filter(email = data['email']).exists()):
                return JsonResponse(
                    {'MESSAGE' : '이미 사용중'}, status = 400)

            else :
                pw = data['password'].encode()
                pw_encrypt = bcrypt.hashpw(pw, bcrypt.gensalt())
                pw_encrypt = pw_encrypt.decode()
                User.objects.create(
                    email      = data['email'],
                    password   = pw_encrypt 
                )
                return JsonResponse(
                    {'MESSAGE' : 'SignUp SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse(
                {'MESSAGE' : 'KEYERROR'}, status = 400)

class SigninView(View):
    def post(self, request):

        try:
            data = json.loads(request.body)

            # 이메일로 로그인 시
            if User.objects.filter(email = data['email']).exists():
                user = User.objects.get(email=data['email'])

                if bcrypt.checkpw(data['password'].encode(), user.password.encode()):
                    token = jwt.encode({'id' : user.id}, SECRET_KEY, ALGORITHM)
                    return JsonResponse({'TOKEN' : token}, status = 200)

                else:
                    return JsonResponse({'MESSAGE' : 'INCORRECT PASSWORD'}, status = 400)

            else:
                return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status = 400)
            
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KeyError'}, status = 400)