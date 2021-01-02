import json

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

        try:
            if not (email and user_name and name and password and phone):
                return JsonResponse(
                    {'MESSAGE' : 'KeyERROR'}, status = 400)

            elif ('@' not in email or '.' not in email):
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
                ).save()
                return JsonResponse(
                    {'MESSAGE' : 'SignUp SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse(
                {'MESSAGE' : 'KEYERROR'}, status = 400)

class SigninView(View):
    def post(self, request):

        data = json.loads(request.body)

        # 변수지정했을때 KeyError발생, 왜지?
        # email      = data['email']
        # phone      = data['phone']
        # user_name  = data['user_name']
        # signin_password   = data['password']

        try:
            # 이메일로 로그인 시
            if 'email' in data.keys():
            #if data.get('email')is not None:
                if User.objects.filter(email = data['email']).exists():
                    if User.objects.get(email = data['email']).password == data['password']:
                        return JsonResponse({'MESSAGE' : 'SignIn SUCCES'}, status = 200)
                    else:
                        return JsonResponse({'MESSAGE' : 'INCORRECT PASSWORD'}, status = 400)
                else:
                    return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status = 400)

            # 휴대폰번호로 로그인 시
            elif 'phone' in data.keys():
            #elif data.get('phone')is not None:
                if User.objects.filter(phone = data['phone']).exists():
                    if User.objects.get(phone = data['phone']).password == data['password']:
                        return JsonResponse({'MESSAGE' : 'SignIn SUCCES'}, status = 200)
                    else:
                        return JsonResponse({'MESSAGE' : 'INCORRECT PASSWORD'}, status = 400)
                else: 
                    return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status = 400)

            # 사용자이름으로 로그인 시
            elif 'user_name' in data.keys():
            #elif data.get('user_name')is not None:
                if User.objects.filter(user_name = data['user_name']).exists():
                    if User.objects.get(user_name = data['user_name']).password == data['password']:
                        return JsonResponse({'MESSAGE' : 'SignIn SUCCES'}, status = 200)
                    else:
                        return JsonResponse({'MESSAGE' : 'INCORRECT PASSWORD'}, status = 400)
                else: 
                    return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status = 400)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KeyError'}, status = 400)

            






        




                
                
