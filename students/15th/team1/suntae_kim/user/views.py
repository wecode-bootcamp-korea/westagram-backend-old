import json
import re
import bcrypt
import jwt

from django.http import JsonResponse
from django.views import View

from user.models import User
from user.utils import LoginAuthorization


# Create your views here.

class SignUpView(View):
# 회원가입 로직 작성필요
    def post(self, request):
        try:
            data     = json.loads(request.body)
            username = data['username']
            password = data['password']

            # 정규 표현식
            username_expression = "^[A-Za-z0-9_]*$"
            password_expression = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}"
            email_expression    = "[^@]+@[^@]+\.[^@]+"
            mobile_expression   = "(010)(-{1}\d{4}-{1}\d{4})"

            #  username check and validation
            if (not re.match(email_expression,username) and not re.match(mobile_expression, username)) and not re.match(username_expression, username):
                return JsonResponse({'MESSAGE' : 'USERNAME_ERROR'})

            # password validation
            elif not re.search(password_expression, password):
                return JsonResponse({'MESSAGE' : 'PASSWORD_ERROR'})

            # 요청한 데이터가 데이터베이스에 있는지 확인 하고, 있는 경우 에러가 발생하게 함.
            # 요청한 데이터가 데이터베이스에 있는지 조회 구현
            elif User.objects.filter(username = username).count() >= 1:
                return JsonResponse({'MESSAGE' : 'ACCOUNT_ERROR'})

                    # 위의 모든 경우가 괜찮은 경우 데이터 베이스 생성
            else:
                user = User.objects.create(
                    username     = username,
                    password     = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()
                )
                return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)


class SignInView(View):

    @LoginAuthorization
    def post(self, request):
        try:
            data     = json.loads(request.body)
            username = data['username']
            password = data['password']

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'})
