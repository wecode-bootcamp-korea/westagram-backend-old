import json
import re
import bcrypt
import jwt

from django.http import JsonResponse
from django.views import View

from user.models import User
from user.utils import LoginAuthorization


class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            username = data['username']
            password = data['password']

            # 정규 표현식
            username_expression = "^[A-Za-z0-9_]*$"
            email_expression    = "[^@]+@[^@]+\.[^@]+"
            password_expression = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}"
            mobile_expression   = "(010)(-{1}\d{4}-{1}\d{4})"

            if (not re.match(email_expression,username) and not re.match(mobile_expression, username)) and not re.match(username_expression, username):
                return JsonResponse({'MESSAGE' : 'USERNAME_OR_PASSWORD_ERROR'}, status=400)

            if not re.search(password_expression, password):
                return JsonResponse({'MESSAGE' : 'USERNAME_OR_PASSWORD_ERROR'}, status=400)

            if User.objects.get(username = username).count() >= 1:
                return JsonResponse({'MESSAGE' : 'ACCOUNT_ALREADY_EXIST'}, status=400)

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
