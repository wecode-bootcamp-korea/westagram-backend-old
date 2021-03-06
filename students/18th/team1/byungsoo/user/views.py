import json, re

from django.views import View
from django.http  import JsonResponse

from .models import User


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

            User.objects.create(email=email, password=password)

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
            
            if User.objects.filter(email=email, password=password).exists()==False:
                return JsonResponse({"message": "INVALID_USER"}, status=401)
            
            return JsonResponse({"message": "SUCCESS"}, status=200)
            
        except json.decoder.JSONDecodeError:
            # http POST http://127.0.0.1:8000/user/login
            return JsonResponse({"message": "데이터가 없거나 Key값이 적절하지 않습니다."})
        
        except KeyError:
            # ex) http POST http://127.0.0.1:8000/user/signup email=""
            return JsonResponse({"message": "하나 이상의 Key값이 적절하지 않거나 존재하지 않습니다."})
        


  