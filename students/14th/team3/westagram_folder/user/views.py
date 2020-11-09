import json
import bcrypt
import jwt
import re
from django.views                import View
from django.http                 import JsonResponse, HttpResponse
from project_westagram.settings  import SECRET_KEY
from .models                     import Account

# 치킨먹고싶다...
class SignUpView(View):
    def post(self, request): #포스트로 받을 시 저장
        data = json.loads(request.body)
        signupdb = Account.objects.all() #유저 테이블정보 다 가져와
        try:        
            user = Account(
                name         = data['name'],
                phone_number = data['phone_number'],
                email        = data['email'],
                password     = data['password'])
            email_valid = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if email_valid.match(data['email']) == None:
                return JsonResponse({"message" : "email_error"}, status = 400)
            elif len(data['password']) < 8 :
                return JsonResponse({"message" : "short_password"}, status = 400)
            elif Account.objects.filter(email = data['email']).exists() or Account.objects.filter(name = data['name']).exists() or Account.objects.filter(phone_number = data['phone_number']).exists() :
                return JsonResponse({"message" : "duplicated_information"}, status = 401)
            else:
                Account.objects.create(
                    name         = data['name'],
                    phone_number = data['phone_number'],
                    email        = data['email'],
                    password     = bcrypt.hashpw(data['password'].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")).save()
                return JsonResponse({"message" : "SUCCESS"}, status = 201)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

    def get(self, request): #겟으로 받을시 유저테이블에 있는것 출력
        account_data = Account.objects.values()
        return JsonResponse({'Account Data' : list(account_data)}, status = 200)

class LoginView(View):
    def post(self, request):
        data        = json.loads(request.body)
        user_password = data['password'] #헷갈릴까바 안썼음

        try:
            if 'name' not in data and 'email' not in data and 'phone_number' not in data:
                return JsonResponse({'message' : 'KEY_ERROR'},   status = 400)
            elif 'password' not in data:
                return JsonResponse({'message' : 'KEY_ERROR'},   status = 400)

            elif Account.objects.filter(email = data['email']).exists():
                exist_user = Account.objects.get(email = data['email'])
                if bcrypt.checkpw(data['password'].encode('UTF-8'), exist_user.password.encode('UTF-8')):
                    token = jwt.encode({'user_id' : exist_user.id}, SECRET_KEY, algorithm='HS256').decode('UTF-8')
                    header = jwt.decode(token, SECRET_KEY, algorithm = 'HS256')
                    print(header)
                    return JsonResponse({'token' : token}, status = 200)
                return JsonResponse({"message" : "INVALID_USER"}, status = 401)
            return JsonResponse({"message" : "No_Exist_User"}, status = 401)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'},  status = 400)
        

    def get(self, request): #get메쏘드로 회원가입된 데이터들을 list형태로 반환
        account_data = Account.objects.values()
        return JsonResponse({'Login' : list(account_data)}, status = 200)
        
