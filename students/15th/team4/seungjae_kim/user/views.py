import json
import re
import bcrypt
import jwt

from django.http  import JsonResponse, HttpResponse
from django.views import View
from user.models  import Users
from my_settings  import SECRET_KEY

def is_valid(text, regex):

    return re.compile(regex).match(text) != None

class UserView(View):    

    def post(self,request):
        
        pw_regex    = '^[A-Za-z0-9@#$%^&+=]{8,}$'
        email_regex = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
     
        data = json.loads(request.body)
        
        # 나중에 프론트엔드 분이랑 협의해서 각 에러별로 상수값 지정하기 !
        # Error_code 3 이런식으로만 Message 보내기로 하
        try:
            
            assert is_valid(data['email'],email_regex), "INVALID_EMAIL_FORMAT"
            assert is_valid(data['password'],pw_regex), "INVALID_PW_FORMAT"

            hased_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            

            if Users.objects.filter(email = data['email']): 
                return JsonResponse({"MESSAGE" : "USER_ALREADY_EXISTS"},status = 400)
                
            else:
                Users.objects.create(email = data["email"],password=hased_password.decode())   
             
                # restapi 시점에서 201은 생성을 의미 !
                return JsonResponse({"MESSAGE" : "SUCCESS"},status =201)

        except KeyError:
            return JsonResponse({'MESSAGE': "KEY_ERROR"},status=400)
        
        except AssertionError as e:
            return JsonResponse({"MESSAGE": f"{e}"}, status = 400)


class SigninView(View):

    def post(self, request):

        data = json.loads(request.body)

        try:
            user = Users.objects.get(email = data['email'])
            
            assert bcrypt.checkpw(data['password'].encode(), user.password.encode())
            
            access_token = jwt.encode({"id":user.id}, SECRET_KEY, algorithm='HS256')
            
            return JsonResponse({'MESSAGE': "SUCCESS","TOKEN": access_token.decode()},status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': "KEY_ERROR"},status=400)

        except Users.DoesNotExist and AssertionError:
            return JsonResponse({'MESSAGE': "INVALID_USER"},status=401)
