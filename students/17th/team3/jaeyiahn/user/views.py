import json

from django.views import View
from django.http  import JsonResponse

from .models import User

MINIMUM_PASSWORD_LENGTH = 8

#회원가입
class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)

            username = data.get('username')
            email    = data.get('email')
            phone    = data.get('phone')
            password = data.get('password')

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



    



