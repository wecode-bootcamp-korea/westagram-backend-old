import json
import bcrypt
import jwt
import re

from django.views                import View
from django.http                 import JsonResponse, HttpResponse
from django.db.models            import Q

from django.conf                 import settings
from .models                     import Account

class SignUpView(View):
    def post(self, request): #포스트로 받을 시 저장
        data = json.loads(request.body)
        try:        
        #    user = Account(
        #        name         = data['name'],
        #        phone_number = data['phone_number'],
        #        email        = data['email'],
        #        password     = data['password']
        #    )
            email_valid      = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            if not email_valid.match(data['email']):
                return JsonResponse({"MESSAGE" : "EMAIL_ERROR, MUST CONTAIN  '@'  and  '.'"}, status = 400)
            elif len(data['password']) < 8:
                return JsonResponse({"MESSAGE" : "SHORT_PASSWORD, MUST BE MORE THAN 7 DIGITS"}, status = 400)
            elif Account.objects.filter(email = data['email']).exists() or Account.objects.filter(name = data['name']).exists() or Account.objects.filter(phone_number = data['phone_number']).exists() :
                return JsonResponse({"MESSAGE" : "DUPLICATED_INFORMATION"}, status = 401)
            Account.objects.create(
            name         = data['name'],
            phone_number = data['phone_number'],
            email        = data['email'],
            password     = bcrypt.hashpw(data['password'].encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8"))
            return JsonResponse({"MESSAGE" : "SUCCESS"}, status = 201)
        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status = 400)

    def get(self, request): #겟으로 받을시 유저테이블에 있는것 출력
        account_data = Account.objects.values()
        return JsonResponse({'ACCOUNT DATA' : list(account_data)}, status = 200)

class LoginView(View):
    def post(self, request):
        data        = json.loads(request.body)
        user_account = Account.objects.filter(Q(name = data['user_account']) | Q(email = data['user_account']) | Q(phone_number=data['user_account']))
            #if 'name' not in data or 'email' not in data or 'phone_number' not in data:
            #    more_info_error = 'ERROR, MUST CONTAINS NAME,EMAIL,PHONE_NUMBER'
            #    return JsonResponse({'MESSAGE' : more_info_error},   status = 400)
        if 'user_account' not in data or 'password' not in data:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
        if not user_account:
            return JsonResponse({"message" : "INVALID_USER"}, status = 400)
        if bcrypt.checkpw(data['password'].encode('UTF-8'), user_account.values()[0]['password'].encode('UTF-8')):
            token = jwt.encode({'user_id' : user_account.values()[0]['id']}, settings.SECRET_KEY, algorithm=settings.ALGORITHM).decode('UTF-8')
            print(token)
            #header = jwt.decode(token, SECRET_KEY, algorithm = ALGORITHM) #header 뽑아볼려고 쓴것
            #user_object = Account.objects.get(id=header['user_id']) # 그 user id 객체 어서오고
            return JsonResponse({'TOKEN' : token}, status = 200)
        return JsonResponse({"MESSAGE" : "INVALID_USER"}, status = 401)