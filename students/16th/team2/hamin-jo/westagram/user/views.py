import json
import re
import bcrypt
import jwt

from django.views import View
from django.http import JsonResponse, HttpResponse

from user.models import User
from my_settings import SECRET_KEY, ALGORITHM
from core        import email_regex, password_regex

class SigninView(View):
    def post(self, request):
        try:
            data           = json.loads(request.body)

            password       = data['password']
            email          = data['email']
            name           = data.get('name')
            phone          = data.get('phone')

            if not (re.search(email_regex,email)):
                return JsonResponse({'MESSAGE': 'INVALID_VALUE'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE': 'EXIST_USER'}, status=400)

            if not (re.search(password_regex, password)):
                return JsonResponse({'MESSAGE': 'INVALID_VALUE'}, status=400)

            encoded_pw      = password.encode('utf-8')
            hashed_pw       = bcrypt.hashpw(encoded_pw, bcrypt.gensalt()).decode('utf-8')

            if phone:
                if User.objects.filter(phone=phone).exists():
                    return JsonResponse({'MESSAGE': 'EXIST_USER'}, status=400)

            User.objects.create(
                email    = email,
                password = hashed_pw,
                name     = name,
                phone    = phone
                )

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERRORS'}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data           = json.loads(request.body)

            email          = data['email']
            user           = User.objects.get(email=email)
            input_password = data['password'].encode('utf-8')
            
            if user is None:
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
            
            if not bcrypt.checkpw(input_password, user.password.encode('utf-8')):
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

            token  = jwt.encode({'user-id':user.id}, SECRET_KEY, ALGORITHM)
            return JsonResponse({"token":token}, status= 200)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERRORS'}, status=400)