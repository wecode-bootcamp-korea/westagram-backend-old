import json

from django.views import View
from django.http  import JsonResponse

from .models      import User


class SignupView(View):

    def get(self,request):
        user_data = User.objects.values()
        return JsonResponse({'user_data': list(user_data)}, status=200)

    def post(self,request):
        try:
            MIN_PASSWORD_LENGHT = 8

            data = json.loads(request.body)

            # username, email, phone이 입력되지 않았다면 None
            username = data['username'] if 'username' in data else None
            email    = data['email']    if 'email'    in data else None
            phone    = data['phone']    if 'phone'    in data else None

            password = data['password']
            
            # username, email, phone이 모두 입력되지 않았을때
            if (username or email or phone) == None:
                return JsonResponse({'MESSAGE': 'KEY ERROR'}, status=400)

            if username != None and User.objects.filter(username=username).exists():
                return JsonResponse({'MESSAGE :':"이미 존재하는 사용자 이름입니다."},status = 400)

            if email    != None and ('@' not in email or '.' not in email):
                return JsonResponse({'MESSAGE :':"EMAIL VALIDATION"},status = 400)
            
            if email    != None and User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE :':"이미 존재하는 이메일입니다."},status = 400)

            if phone    != None and User.objects.filter(phone=phone).exists():
                return JsonResponse({'MESSAGE :':"이미 존재하는 전화번호입니다."},status = 400)

            if len(password) < MIN_PASSWORD_LENGHT:
                return JsonResponse({'MESSAGE :':"PASSWORD VALIDATION"},status = 400)

            User.objects.create(
                username = username,
                email    = email,
                phone    = phone,
                password = password
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200) 
        except KeyError:
            return JsonResponse({'MESSAGE': "KEY ERROR"}, status=400)


class LoginView(View):
    def get(self,request):
        try:
            data = json.loads(request.body)
            user = User()

            if   'username' in data:
                user = User.objects.get(username=data['username'])
            elif 'email'    in data:
                user = User.objects.get(email=data['email'])
            elif 'phone'    in data:
                user = User.objects.get(phone=data['phone'])

            if user.password == data['password']:
                return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)
            return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
        except KeyError:
            return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
         