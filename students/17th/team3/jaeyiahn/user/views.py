import json

from django.views import View
from django.http  import JsonResponse

from .models import User

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
                return JsonResponse({'message': '중복된 email'}, status=400)
            
            if '@' and '.' not in email:
                return JsonResponse({'message': '잘못된 email형식'}, status=400)
            
            if len(password) < 8:
                return JsonResponse({'message': '비밀번호는 8자리 이상'}, status=400)

            if User.objects.filter(username=data['username']).exists():
                    return JsonResponse({'message': '중복된 username'}, status=400)

            if User.objects.filter(phone=data['phone']).exists():
                    return JsonResponse({'message': '중복된 phone number'}, status=400)

            User.objects.create(username=username, email=email, phone=phone, password=password)
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)



    



