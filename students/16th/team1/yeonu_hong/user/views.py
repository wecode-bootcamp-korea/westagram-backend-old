import json
from django.http  import JsonResponse
from django.views import View
from .models      import User

# 회원가입
class SignUpView(View):
    def post(self, request): 
        try:
            data      = json.loads(request.body)
            name      = data['name']
            phone     = data['phone']
            email     = data['email']
            password  = data['password']

            if User.objects.filter(name=data["name"]).exists():
                name_dup  = User.objects.filter(name=data["name"])
                return JsonResponse({'message': '이미 사용중인 name'}, status=400)
            if User.objects.filter(phone=data["phone"]):
                phone_dup = User.objects.filter(phone=data["phone"])
                return JsonResponse({'message': '이미 사용중인 phone'}, status=400)
            if User.objects.filter(email=data["email"]):
                email_dup = User.objects.filter(email=data["email"])
                return JsonResponse({'message': '이미 사용중인 email'}, status=400)


            if len(password) > 8:
                return JsonResponse({'message': '비밀번호 길이는 8글자 이상'}, status=400)


            User(
                name     = name,
                password = password,
                phone    = phone,
                email    = email).save()
    
            return JsonResponse({'message': 'SUCCESS'}, status=200)
            
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


