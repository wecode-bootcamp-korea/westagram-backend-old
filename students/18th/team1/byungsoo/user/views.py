import json, re, bcrypt, jwt

from django.views import View
from django.http  import JsonResponse

from .models     import User
from my_settings import SECRET_KEY


class SignUpView(View):
    def post(self, request):
        
        try:
            data = json.loads(request.body)

            email    = data['email']
            password = data['password']

            if not email or not password:
                """ email="" password=""과 같이 아무것도 입력되지 않은 값이 왔을 때 KEY_ERROR를 발생시킵니다."""
                return JsonResponse({"message": "KEY_ERROR"}, status=400)

            regex_for_email = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            
            if not regex_for_email.match(email):
                return JsonResponse({"message": "이메일 형식을 지켜주세요."}, status=400)

            if len(password) < 8:
                return JsonResponse({"message": "비밀번호가 너무 짧습니다."}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "이미 존재하는 이메일입니다."}, status=409)

            encoded_password  = password.encode('utf-8')
            hashed_password   = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
            decoded_hashed_pw = hashed_password.decode('utf-8') 

            User.objects.create(email=email, password=decoded_hashed_pw)

            return JsonResponse({"message":"SUCCESS"}, status=200)
        
        except ValueError:
            # http POST http://127.0.0.1:8000/user/signup
            return JsonResponse({"message": "아무 데이터도 보내지 않았습니다."})
        
        except KeyError:
            # ex) http POST http://127.0.0.1:8000/user/signup email=""
            return JsonResponse({"message": "Key가 존재하지 않습니다."})

        

class LogInView(View): 
    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data["email"]
            password = data["password"]

            if not email or not password:
                """ email="" password=""과 같이 둘 중 하나의 key값에 아무것도 입력되지 않은 값이 왔을 때 KEY_ERROR를 발생시킵니다."""
                return JsonResponse({"message": "KEY_ERROR"}, status=400)
            
            hashed_password_mysql = User.objects.get(email=email).password

            if User.objects.filter(email=email, password=hashed_password_mysql).exists()==False:
                return JsonResponse({"message": "INVALID_USER"}, status=401)
            
            
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password_mysql.encode('utf-8')):
                user_id     = User.objects.get(email=email).id
                encoded_jwt = jwt.encode( {'user-id': user_id}, SECRET_KEY, algorithm='HS256')

            
            return JsonResponse({"message": "SUCCESS", 'access-token': encoded_jwt}, status=200)
            
        except json.decoder.JSONDecodeError:
            # http POST http://127.0.0.1:8000/user/login
            return JsonResponse({"message": "데이터가 없거나 Key값이 적절하지 않습니다."})
        
        except KeyError:
            # ex) http POST http://127.0.0.1:8000/user/signup email=""
            return JsonResponse({"message": "하나 이상의 Key값이 적절하지 않거나 존재하지 않습니다."})
        


  