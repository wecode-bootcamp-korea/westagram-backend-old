import json
import re

from django.http   import JsonResponse
from django.views  import View
from user.models   import User

class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)

        email      = data['email']
        phone      = data['phone']
        name       = data['name']
        user_name  = data['user_name']
        password   = data['password']

        # email 정규표현식
        vali_email = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        validate_email=re.compile(vali_email)

        try:
            if not (email and user_name and name and password and phone):
                return JsonResponse(
                    {'MESSAGE' : 'KeyERROR'}, status = 400)
            
            elif not validate_email.match(email):
                return JsonResponse(
                    {'MESSAGE' : '잘못된 email형식'}, status = 400)

            elif len(password) < 8 :
                return JsonResponse(
                    {'MESSAGE' : 'password는 8자리 이상'}, status = 400)

            elif (User.objects.filter(email = email).exists() 
            or User.objects.filter(user_name = user_name).exists()):
                return JsonResponse(
                    {'MESSAGE' : '이미 사용중'}, status = 400)

            else :
                User.objects.create(
                    email      = email,
                    phone      = phone,
                    name       = name,
                    user_name  = user_name,
                    password   = password 
                )
                return JsonResponse(
                    {'MESSAGE' : 'SignUp SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse(
                {'MESSAGE' : 'KEYERROR'}, status = 400)

class SigninView(View):
    def post(self, request):

        data = json.loads(request.body)

        # 변수지정했을때 KeyError발생, 왜지?
        # 변수지정을 해줬을 때 에러가 뜬 이유 : 변수를 지정해 줬으나 
        # http로 받아온 정보에는 해당 되는 변수가 없었기 때문에 에러가 발생한 것
        # 받아온 데이터를 변수로 지정하고 싶다면 아래와 같이 해당 데이터가 있을 때 변수로 가져오는 형식으로 바꾸면 된다.
        if 'email' in data.keys():
            email      = data['email']
        if 'phone' in data.keys():
            phone      = data['phone']
        if 'user_name' in data.keys():
            user_name  = data['user_name']
        if 'password' in data.keys():
            password = data['password']
       
        try:
            # 이메일로 로그인 시
            if 'email' in data.keys():
            #if data.get('email')is not None:
                if User.objects.filter(email = email).exists():
                    if User.objects.get(email = email).password ==  password:
                        return JsonResponse({'MESSAGE' : 'SignIn SUCCES'}, status = 200)
                    else:
                        return JsonResponse({'MESSAGE' : 'INCORRECT PASSWORD'}, status = 400)
                else:
                    return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status = 400)

            # 휴대폰번호로 로그인 시
            elif 'phone' in data.keys():
            #elif data.get('phone')is not None:
                if User.objects.filter(phone = phone).exists():
                    if User.objects.get(phone = phone).password == password:
                        return JsonResponse({'MESSAGE' : 'SignIn SUCCES'}, status = 200)
                    else:
                        return JsonResponse({'MESSAGE' : 'INCORRECT PASSWORD'}, status = 400)
                else: 
                    return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status = 400)

            # 사용자이름으로 로그인 시
            elif 'user_name' in data.keys():
            #elif data.get('user_name')is not None:
                if User.objects.filter(user_name = user_name).exists():
                    if User.objects.get(user_name = user_name).password == password:
                        return JsonResponse({'MESSAGE' : 'SignIn SUCCES'}, status = 200)
                    else:
                        return JsonResponse({'MESSAGE' : 'INCORRECT PASSWORD'}, status = 400)
                else: 
                    return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status = 400)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KeyError'}, status = 400)

            






        




                
                
