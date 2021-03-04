import json, re

from django.views import View
from django.http  import JsonResponse

from .models import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        email    = data['email']
        password = data['password']
        
        if not email or not password:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        regex_for_email = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        
        if not regex_for_email.match(email):
            return JsonResponse({"message": "이메일 형식을 지켜주세요22."}, status=400)

        if len(password) < 8:
            return JsonResponse({"message": "비밀번호가 너무 짧습니다."}, status=400)
        
        if User.objects.filter(email=email).first():
            return JsonResponse({"message": "이미 존재하는 이메일입니다."}, status=409)

        User.objects.create(email=email, password=password)

        return JsonResponse({"message":"SUCCESS"}, status=200)


class LogInView(View):
    