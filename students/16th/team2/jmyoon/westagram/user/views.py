import json
import re
import bcrypt
import jwt

from django.http   import JsonResponse
from django.views  import View

from user.models   import User
from my_settings   import SECRET_KEY

class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)

        #email      = data['email']
        #phone      = data['phone']
        #name       = data['name']
        #user_name  = data['user_name']
        #password   = data['password']
        
        # email 정규표현식
        vali_email = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        validate_email=re.compile(vali_email)

        try:
            if not data['email']:
                return JsonResponse(
                    {'MESSAGE' : 'KeyERROR'}, status = 400)
            # if not (email or phone):
            #     return JsonResponse(
            #         {'MESSAGE' : 'KeyERROR'}, status = 400)


            # elif not (name and user_name):
            #     return JsonResponse(
            #         {'MESSAGE' : 'KeyERROR'}, status = 400)
            
            elif not validate_email.match(data['email']):
                return JsonResponse(
                    {'MESSAGE' : '잘못된 email형식'}, status = 400)

            elif len(data['password']) < 8 :
                return JsonResponse(
                    {'MESSAGE' : 'password는 8자리 이상'}, status = 400)

            elif (User.objects.filter(email = data['email']).exists()):
                return JsonResponse(
                    {'MESSAGE' : '이미 사용중'}, status = 400)
            # elif (User.objects.filter(email = email).exists() 
            # or User.objects.filter(user_name = user_name).exists()):
            #     return JsonResponse(
            #         {'MESSAGE' : '이미 사용중'}, status = 400)

            else :
                pw = data['password'].encode()
                pw_encrypt = bcrypt.hashpw(pw, bcrypt.gensalt())
                pw_encrypt = pw_encrypt.decode()
                User.objects.create(
                    email      = data['email'],
                    #phone      = phone,
                    #name       = name,
                    #user_name  = user_name,
                    password   = pw_encrypt 
                )
                return JsonResponse(
                    {'MESSAGE' : 'SignUp SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse(
                {'MESSAGE' : 'KEYERROR'}, status = 400)

class SigninView(View):
    def post(self, request):

        #data = json.loads(request.body)

        # if 'email' in data.keys():
        #     email      = data['email']
        # if 'phone' in data.keys():
        #     phone      = data['phone']
        # if 'user_name' in data.keys():
        #     user_name  = data['user_name']
        # if 'password' in data.keys():
        #     password   = data['password']
       
        try:
            data = json.loads(request.body)

            # 이메일로 로그인 시
            if 'email' in data.keys():
                if User.objects.filter(email = data['email']).exists():
                    user=User.objects.get(email=data['email'])
                    if bcrypt.checkpw(data['password'].encode(), user.password.encode()):
                        token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm='HS256')
                        return JsonResponse({'TOKEN' : token}, status = 200)
                    else:
                        return JsonResponse({'MESSAGE' : 'INCORRECT PASSWORD'}, status = 400)
                else:
                    return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status = 400)
            else:
                return JsonResponse({'MESSAGE' : 'KeyError'}, status = 400)

            
        except:
            return JsonResponse({'MESSAGE' : 'KeyError'}, status = 400)

            # 휴대폰번호로 로그인 시
            # elif 'phone' in data.keys():
            #     if User.objects.filter(phone = phone).exists():
            #         user=User.objects.get(phone=phone)
            #         if bcrypt.checkpw(password.encode(), user.password.encode()):
            #             token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm='HS256')
            #             return JsonResponse({'TOKEN' : token}, status = 200)
            #         else:
            #             return JsonResponse({'MESSAGE' : 'INCORRECT PASSWORD'}, status = 400)
            #     else: 
            #         return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status = 400)

            # # 사용자이름으로 로그인 시
            # elif 'user_name' in data.keys():
            #     if User.objects.filter(user_name = user_name).exists():
            #         user=User.objects.get(user_name=user_name)
            #         if bcrypt.checkpw(password.encode(), user.password.encode()):
            #             token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm='HS256')
            #         else:
            #             return JsonResponse({'MESSAGE' : 'INCORRECT PASSWORD'}, status = 400)
            #     else: 
            #         return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status = 400)

        # except KeyError:
        #     return JsonResponse({'MESSAGE' : 'KeyError'}, status = 400)

# def check_pw(item):
#     signin_user = User.objects.get(item=data['item'])
#     if bcrypt.checkpw(data['password'].encode(), signin_user.password.encode()):
#         token = jwt.encode({'id' : signin_user.id}, SECRET_KEY, algorithm='HS256')
#         return JsonResponse({'TOKEN' : token}, status = 200)
#     else:
#         return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status = 400)



        




                
                
