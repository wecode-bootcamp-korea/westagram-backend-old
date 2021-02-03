import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .models import User

MINIMUM_PASSWORD_LENGTH = 8

#회원가입
class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)

            username = data.get('username')
            phone    = data.get('phone')
            email    = data['email']
            password = data['password']
            
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'EMAIL_EXISTS'}, status=400)
            
            if '@' and '.' not in email:
                return JsonResponse({'message': 'EMAIL_INVALID'}, status=400)

            if len(password) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({'message': 'SHORT_PASSWORD'}, status=400)

            if User.objects.filter(username=data['username']).exists():
                return JsonResponse({'message': 'USERNAME_EXISTS'}, status=400)

            if User.objects.filter(phone=data['phone']).exists():
                return JsonResponse({'message': 'PHONE_EXISTS'}, status=400)

            User.objects.create(username=username, email=email, phone=phone, password=password)
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

#로그인    
class LogInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            username = data.get('username')
            phone    = data.get('phone')
            email    = data.get('email')
            password = data['password']
            
            if User.objects.filter(Q(email=email)|Q(username=username)|Q(phone=phone)).exists():
                if User.objects.get(Q(email=email)|Q(username=username)|Q(phone=phone)).password == password:
                    return JsonResponse({'message': 'SUCCESS'}, status=200)
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)
            return JsonResponse({'message': 'INVALID_USER'}, status=401)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)