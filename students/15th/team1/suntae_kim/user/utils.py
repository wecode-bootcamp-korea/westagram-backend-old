import json
import os
import sys
import jwt
import bcrypt

from user.models import User
from django.http import JsonResponse

from my_settings import SECRET_KEY

"""
class LoginAuthorization:s
    def __init__(self, function):  # 호출할 함수를 인스턴스의 초깃값으로 받음
        self.function = function   # 호출할 함수를 속성 function에 저장

    def __call__(self, request, *args, **kwargs): # 인스턴스를 함수처럼 호출하게 해줌,
    # 클래스형 데코레이터를 쓰기위해서는 __call_메소드를 반드시 작성해야함
        print('================user.token 호출 =====================')
        token = request.headers.get('Authorization') # 클라이언트의 headers 에서 Authorization 을 가져옴
        print('====================headers 호출=====================')
        print('request.header:', request.headers)
        print('=================headers 호출 종료===================')
        print('token:', token)
        print('==============user.token 호출 종료===================')


        try:
            if token:
                token_payload = jwt.decode(token, SECRET_KEY, algorithms='HS256' ) # Authorization 가져오기
                print('token_payload:', type(token_payload['username']))
                user_check = User.objects.get(username=token_payload['username'])
                user_check_name = token_payload['username']
                print(user_check_name)
                print(user_check)
                request.user = user_check
                print(request.user)
                return self.function(self, request, *args, **kwargs)

            return JsonResponse({ 'MESSAGE' : 'SIGNIN_FIRST' })

        except Exception as e:
            JsonResponse({'ERROR' : e})


 #       except Exception as e:
 #           return JsonResponse({ 'INVALID_USER_SIGNIN_FIRST' : e })
"""


def LoginAuthorization(function):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
#        print('===========token 호출===========')
#        print('token :', token)
        token_payload = jwt.decode( token, SECRET_KEY, algorithms='HS256' )
#        print('===========token payload 호출===========')
#        print(token_payload)
#        print('===========호출종료===========')
        user_check = User.objects.get(username=token_payload['username'])
        user_check_name = token_payload['username']
#        print('request:', request)
        request.user = user_check
#        print('user_check_name: ', user_check_name)
#        print('request.user: ', request.user)
        return function(self, request, *args, **kwargs)
    return wrapper






