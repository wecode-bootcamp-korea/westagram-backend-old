import json
import re
import bcrypt
import jwt

import my_settings

from django.views import View
from django.http import JsonResponse
from django.db.models import Q

from share.utils import (
                    #getUserID,
                    #checkRequestBody,
                    #checkAuthorization,
                    checkAuthDecorator,
                    checkRequestBodyDecorator,
                    getUserIDFromToken,
                    )
from .models import (
                User,
                Follow,
                )


class RegistView(View):
    @checkRequestBodyDecorator
    def post(self, request):
        data         = json.loads(request.body)
        
        if not 'name' in data or ('phone_number' in data and not 'email' in data):
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        # email이 password에 대해 정규식 포맷 생성
        email_pattern       = re.compile("\w+@\w+.+\w+")
        password_pattern    = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$")
        
        if data['name'] == '':
            return JsonResponse({"message":"name invalidation"}, status=400)
        # 정규식으로 email, password 체크
        if not email_pattern.search(data['email']):
            return JsonResponse({"message":"email invalidation"}, status=400)
        if not password_pattern.search(data['password']):
            return JsonResponse({"message":"password invalidation"}, status=400)

        # 회원가입시 중복되는 전화번호, 사용자 이름, 이메일이 있으면 에러 메시지 응답.
        #if User.objects.filter(name=data['name']).exists():
        #    return JsonResponse({"message":"same name is already exist."}, status=400)
        if User.objects.filter(name=data['phone_number']).exists():
            return JsonResponse({"message":"same phone_number is already exist."}, status=400)
        if User.objects.filter(name=data['email']).exists():
            return JsonResponse({"message":"same email is already exist."}, status=400)
        
        hashed_pw = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())

        User(
                name            = data['name'],
                email           = data['email'],
                phone_number    = data['phone_number'],
                password        = hashed_pw.decode(),
                ).save()

        return JsonResponse({"message":"SUCCESS"}, status=200)

    def get(self, request):
        return JsonResponse({"message":"Hello"}, status=200)

class LoginView(View):
    @checkRequestBodyDecorator
    def post(self, request):
        data        = json.loads(request.body)
        login_info  = {'account':'', 'password':''}

        if not 'account' in data or not 'password' in data:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        login_info['account']   = data['account']
        login_info['password']  = data['password']
        
        try:
            account     = User.objects.get(Q(name=login_info['account'])
                                           | Q(email=login_info['account'])
                                           | Q(phone_number=login_info['account']))
        
            if bcrypt.checkpw(login_info['password'].encode(), account.password.encode()):
                token       = jwt.encode({"user_id":account.id}, my_settings.SECRET['secret'],\
                                        algorithm='HS256')

                return JsonResponse({"message":token.decode()}, status=200)

            return JsonResponse({"message":"INVALID_USER"}, status=401)

        except Exception:
            return JsonResponse({"message":"INVALID_USER"}, status=401)

class FollowUser(View):
    @checkAuthDecorator
    @checkRequestBodyDecorator
    def post(self, request):
        data             = json.loads(request.body)
        user_id          = getUserIDFromToken(data['token'])
        
        if not user_id:
            return JsonResponse({"message":"[token] is not allowed."}, status=400)
        
        FOLLOWED_USER_ID = 'followed_user_id'

        if not FOLLOWED_USER_ID in data:
            return JsonResponse({"message":"[followed_user_id] is empty"}, status=400)

        followed_user_id = data[FOLLOWED_USER_ID]

        if not User.objects.filter(id=followed_user_id).exists():
            return JsonResponse({"message":"followed user is not exist."}, status=400)
        
        follow = Follow.objects.filter(followed_user_id=followed_user_id, following_user_id=user_id)
        
        if not follow:            
            Follow.objects.create(followed_user_id=followed_user_id, following_user_id=user_id)
        else:
            follow.delete()            
        
        return JsonResponse({"message":"SUCCESS"}, status=201)


