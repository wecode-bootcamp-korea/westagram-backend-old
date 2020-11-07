import json
import re
from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from share.utils import (
                    getUserID,
                    checkRequestBody,
                    )
from .models import (
                Users,
                Follows,
                )


class RegistView(View):
    def post(self, request):
        '''
        try:
            data            = json.loads(request.body)
        except Exception as ex:
            return JsonResponse({"message":"You request with wrong format."}, status=400)
        '''
        hasProblem = checkRequestBody(request)
        if hasProblem:
            return hasProblem

        user_account        = {'name':'','phone_number':'','email':''}
        
        if 'name' in data:
            user_account['name']            = data['name']
        if 'phone_number' in data:
            user_account['phone_number']    = data['phone_number']
        if 'email' in data:
            user_account['email']           = data['email']
        
        # 입력 정보 중 name, phone_number, email 정보가 하나도 없거나 password 정보가 없으면 경고 response.
        if user_account['name'] == ''\
            or (user_account['phone_number'] == '' and user_account['email'] == '')\
            or not 'password' in data:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)
        

        # email이 password에 대해 정규식 포맷 생성
        email_pattern       = re.compile("\w+@\w+.+\w+")
        password_pattern    = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$")
        
        # 정규식으로 email, password 체크
        if email_pattern.search(data['email']) == None:
            return JsonResponse({"message":"Error","validation":"email validation"}, status=400)
        if password_pattern.search(data['password']) == None:
            return JsonResponse({"message":"Error","validation":"password validation"}, status=400)

        # 회원가입시 중복되는 전화번호, 사용자 이름, 이메일이 있으면 에러 메시지 응답.
        if Users.objects.filter(name=user_account['name']).exists():
            return JsonResponse({"message":"same name is already exist."}, status=400)
        if Users.objects.filter(name=user_account['phone_number']).exists():
            return JsonResponse({"message":"same phone_number is already exist."}, status=400)
        if Users.objects.filter(name=user_account['email']).exists():
            return JsonResponse({"message":"same email is already exist."}, status=400)

        Users(
                name            = user_account['name'],
                email           = user_account['email'],
                phone_number    = user_account['phone_number'],
                password        = data['password'],
                ).save()

        return JsonResponse({"message":"SUCCESS"}, status=200)

    def get(self, request):
        return JsonResponse({"message":"Hello"}, status=200)

class LoginView(View):
    def post(self, request):
        '''
        try:
            data        = json.loads(request.body)
        except Exception as ex:
            return JsonResponse({"message":"You request with wrong format."}, status=400)
        '''
        hasProblem = checkRequestBody(request)
        if hasProblem:
            return hasProblem
        
        login_info      = {'account':'', 'password':''}
        
        if not 'account' in data or not 'password' in data:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

        login_info['account']   = data['account']
        login_info['password']  = data['password']
        
        if Users.objects.filter(Q(name=login_info['account'])
                                | Q(email=login_info['account'])
                                | Q(phone_number=login_info['account'])
                                , password=login_info['password']).exists():
            return JsonResponse({"message":"SUCCESS"}, status=200)
        else:
            return JsonResponse({"message":"INVALID_USER"}, status=401)
        


class Follow(View):
    def post(self, request):
        hasProblem = checkRequestBody(request)
        if hasProblem:
            return hasProblem

        #checkRequestBody(request)
        #data = json.loads(request.body)

        FOLLOWED_USER_ID = 'followed_user_id'

        if not "account" in data or not FOLLOWED_USER_ID in data:
            return JsonResponse({"message":"[account] or [followed_user_id] is empty"}, status=400)

        user_id          = getUserID(data['account'])
        followed_user_id = data[FOLLOWED_USER_ID]

        if not Users.objects.filter(id=followed_user_id).exists():
            return JsonResponse({"message":"followed user is not exist."}, status=400)
       
        if not Follows.objects.filter(followed_user_id=followed_user_id, following_user_id=user_id):
            Follows.objects.create(followed_user_id=followed_user_id, following_user_id=user_id)
        
        return JsonResponse({"message":"SUCCESS"}, status=201)





