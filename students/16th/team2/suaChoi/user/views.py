import json
import re
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View

from .models     import User
from .utils      import check_user
from my_settings import SECRET


class SignupView(View):

    def post(self, request):

        try:
            data     = json.loads(request.body)
            name     = data.get('name')
            email    = data['email']
            phone    = data.get('phone')
            password = data['password']

            email_rule = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            if not email and password:
                return JsonResponse({"message": "KEY_ERRPR"}, status=400)

            if len(password) <  8:
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)

            if not email_rule.match(email):
                return JsonResponse({"message": "INVALID_EMAIL"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "EXIST_EMAIL"}, status=400)

            encoded_pw = password.encode('utf-8')
            hashed_pw = bcrypt.hashpw(encoded_pw, bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                 name     = name,
                 email    = email,
                 password = hashed_pw,
                 phone    = phone
             )
            return JsonResponse({"message": "SUCCESS"}, status=200)

        except:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class LoginView(View):

    def post(self, request):

        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']


            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                user_password = user.password
                if bcrypt.checkpw(password.encode('utf-8'), user_password.encode('utf-8')) is True:
                    payload={"user_id": user.id}
                    token=jwt.encode(payload, SECRET, algorithm='HS256')
                    return JsonResponse({"token":token}, status=200)
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=401)
            return JsonResponse({"message": "INVALID_EMAIL"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except:
            return JsonResponse({"message": "ERROR"}, status=500)


