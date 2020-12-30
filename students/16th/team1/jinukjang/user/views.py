import json

from django.views import View
from django.http  import JsonResponse

from .models      import User


class SignupView(View):

    def get(self,request):
        user_data = User.objects.values()
        return JsonResponse({'user_data': list(user_data)}, status=200)

    def post(self,request):
        MIN_PASSWORD_LENGHT = 8

        data = json.loads(request.body)

        # username, email, phone이 입력되지 않았다면 None
        username = data['username'] if 'username' in data else None
        email    = data['email']    if 'email'    in data else None
        phone    = data['phone']    if 'phone'    in data else None
        
        # username, email, phone이 모두 입력되지 않았거나, 비밀번호가 입력되지 않았을때 
        if (username or email or phone) == None or 'password' not in data:
            return JsonResponse({'MESSAGE': 'KEY ERROR'}, status=400)

        if username != None and User.objects.filter(username=username).exists():
            return JsonResponse({'MESSAGE :':"이미 존재하는 사용자 이름입니다."},status = 400)

        if email    != None and ('@' not in email or '.' not in email):
            return JsonResponse({'MESSAGE :':"EMAIL VALIDATION"},status = 400)
        
        if email    != None and User.objects.filter(email=email).exists():
            return JsonResponse({'MESSAGE :':"이미 존재하는 이메일입니다."},status = 400)

        if phone    != None and User.objects.filter(phone=phone).exists():
            return JsonResponse({'MESSAGE :':"이미 존재하는 전화번호입니다."},status = 400)

        password = data['password']

        if len(password) < MIN_PASSWORD_LENGHT:
            return JsonResponse({'MESSAGE :':"PASSWORD VALIDATION"},status = 400)

        User.objects.create(
            username = username,
            email    = email,
            phone    = phone,
            password = password
        )
    
        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200) 

class LoginView(View):
    def get(self,request):
        data = json.loads(request.body)

        login_user = User.objects.all()
        
        username, email, phone = None, None, None
        
        if 'username' in data:
            username   = data['username']
            login_user = login_user.filter(username=username)

        if 'email'    in data:
            email      = data['email']
            login_user = login_user.filter(email=email)

        if 'phone'    in data:
            phone      = data['phone']
            login_user = login_user.filter(phone=phone)

        # username, email, phone이 모두 입력되지 않았거나, 비밀번호가 입력되지 않았을때 
        if (username or email or phone) == None or 'password' not in data:
            return JsonResponse({'MESSAGE': 'KEY ERROR'}, status=400)

        if login_user[0].password == data['password']:
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
         