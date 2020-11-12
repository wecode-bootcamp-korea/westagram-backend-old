import json
import re
import bcrypt
import jwt

from django.views      import View
from django.http       import JsonResponse,request
from django.db.models  import Q

from .models           import User
from westa.my_settings import SECRET_KEY


class RegisterView(View):
   
    def post(self, request):
        data = json.loads(request.body)
        email_analysis= re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

        try:
            # 비밀 번호 8자리 미만일 경우
            if len(data['password']) < 8:
                return JsonResponse({"message" : "PW_ERROR"}, status=400)

            # 이메일 형식 지키지 않았을 경우
            if not (email_analysis.match(data['email']) !=None) :
                return JsonResponse({"message" : "EMAIL_ERROR"}, status=400)  

            # 중복된 row값이 들어갈 경우        
            if User.objects.filter(name = data['name'])\
                                   or User.objects.filter(email = data['email'])\
                                   or User.objects.filter(telephone = data['telephone']):
                return JsonResponse({"message" : "OVERLAP_ERROR"}, status=400)    

            User(
                name      = data['name'],
                telephone = data['telephone'], 
                password  = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode(), 
                email     = data['email']
                ).save()            
            return JsonResponse({"message" : "success"}, status=201)

        except  KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=401)


class LoginView(View):
     def post(self, request):
        data = json.loads(request.body)

        # 아이디, 이메일 또는 전화번호 없을 경우
        if 'user_account' not in data or ('password' not in data):
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

        user_account = User.objects.filter(Q(name = data['user_account']) | Q(email = data['user_account']) | Q(telephone=data['user_account']))

        # 계정이 없을 경우
        if not user_account :
            return JsonResponse({"message" : "INVALID_USER"}, status = 400)
        
        input_password =data['password'].encode('utf-8')
        #비밀번호가 맞지 않을 경우
        if bcrypt.checkpw(input_password,user_account.values()[0]['password'].encode('utf-8')):
            token = jwt.encode({'id' : user_account.values()[0]['id']}, SECRET_KEY['secret'], algorithm='HS256').decode('utf-8')

            return JsonResponse({"Authorization" : token}, status = 200)

        return JsonResponse({"message" : "INVALID_USER"}, status = 400)