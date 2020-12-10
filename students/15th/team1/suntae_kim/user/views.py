import json
import re
import bcrypt
import jwt

from django.http import JsonResponse
from django.views import View

from user.models import User
from my_settings import SECRET_KEY, ALGORITHM
from user.utils  import LoginAuthorization


class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            username = data['username']
            password = data['password']

            REGEX_NAME     = "^[A-Za-z0-9_]*$"
            REGEX_EMAIL    = "[^@]+@[^@]+\.[^@]+"
            REGEX_PASSWORD = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}"
            REGEX_MOBILE   = "(010)(-{1}\d{4}-{1}\d{4})"

            if (not re.match(REGEX_EMAIL,username) and not re.match(REGEX_MOBILE, username)) and not re.match(REGEX_NAME, username):
                return JsonResponse({'MESSAGE' : 'USERNAME_OR_PASSWORD_ERROR'}, status=400)

            if not re.search(REGEX_PASSWORD, password):
                return JsonResponse({'MESSAGE' : 'USERNAME_OR_PASSWORD_ERROR'}, status=400)

            if User.objects.filter(username = username).exists():
                return JsonResponse({'MESSAGE' : 'ACCOUNT_ALREADY_EXIST'}, status=400)

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
            data            = json.loads(request.body)
            username        = data['username']
            password        = data['password'].encode('utf-8')
            user_info       = User.objects.get( username = username )
            user_id         = user_info.id
            user_password   = user_info.password
            hashed_password = user_password.encode( 'utf-8' )

            if bcrypt.checkpw( password, hashed_password ):
                access_token = jwt.encode(
                    {
                     'user_id' : user_id,
                     'username': username
                    }, SECRET_KEY, algorithm = ALGORITHM).decode('utf-8')
                return JsonResponse({'TOKEN' : access_token})

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
