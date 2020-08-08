import json

from django.core.exceptions import ValidationError
from django                 import forms
from django.views           import View
from django.http            import JsonResponse

from .models                import User

class SignUpView(View):
    """
        1. 이메일이나 패스워드 키가 전달되지 않았을 시,
        {"message": "KEY_ERROR"}, status code 400 을 반환
        2. 회원가입시 이메일 @와 .이 필수 포함.
        3. 회원가입시 비밀번호 8자리 이상이어야 함.
        4. 회원가입시 동일한 전화번호나 사용자 이름, 이메일을 사용하지않음
        """
    def post(self, request):
        data       = json.loads(request.body)
        users_info = User.objects.all()

        try:
            signup_user = User(
                name         = data['name'],
                email        = data['email'],
                password     = data['password'],
                phone_number = data['phone_number']
            )
            if users_info.filter(name = data['name']):
                return JsonResponse({'message': 'already exsit name'})

            elif users_info.filter(phone_number = data['phone_number']):
                return JsonResponse({'message': 'already exsit phone_number'})
            
            elif users_info.filter(email = data['email']):
                return JsonResponse({'message': 'already exsit email'})
            signup_user.full_clean()

        except ValidationError:
            return JsonResponse({'message': 'INVALID_PASSWORD_OR_EMAIL'}, status = 400)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        signup_user.save()
        return JsonResponse({'message':'SUCCESS'}, status=200)
    
    def get(self, request):
        user_data = User.objects.values()

        return JsonResponse({'users':list(user_data)}, status=200)

class LogInView(View):
    def post(self, request):
        data       = json.loads(request.body)
        
        try:
            login_user = User(
                name         = data['name'],
                email        = data['email'],
                password     = data['password'],
            )
            if User.objects.filter(name = login_user.name):
                # return JsonResponse({"message": "what"}, status=200)
                account = User.objects.get(name = login_user.name)
                # return JsonResponse({"message": "good"}, status=200)
                if account.password == login_user.password:
                    return JsonResponse({"message": "SUCCESS"}, status=200)
                return JsonResponse({"message": "INVALID_USER"}, status=401)
            return JsonResponse({"message": "INVALID_USER"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
    
    def get(self, request):
        user_data = User.objects.values()

        return JsonResponse({"users":list(user_data)}, status=200)