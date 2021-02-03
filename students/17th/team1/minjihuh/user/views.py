import json
import re
import bcrypt
import jwt

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.db.models import Q

from user.models   import (
    User
)
from westagram.my_settings import SECRET_KEY, ALGORITHM

email_regex              = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
password_regex           = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
phone_regex              = re.compile(r'[0-9]{3}-[0-9]{4}-[0-9]{4}')
MINIMUM_PASSWORD_LENGTH  = 8

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            name                     = data['name']
            phone                    = data['phone']
            email                    = data['email']
            password                 = data['password']
            username                 = data['username']

            if name == "":
                return JsonResponse({"MESSAGE" : "NAME_REQUIRED"}, status=400)

            if phone == "" and email == "":
                return JsonResponse({"MESSAGE" : "EMAIL_OR_PHONE_NUMBER_REQUIRED"}, status=400)

            if username == "":
                return JsonResponse({"MESSAGE" : "USERNAME_REQUIRED"}, status=400)

            if password == "":
                return JsonResponse({"MESSAGE" : "PASSWORD_REQUIRED"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"MESSAGE": "EMAIL_EXISTS"}, status=400)
                
            if User.objects.filter(username=username).exists():
                return JsonResponse({"MESSAGE" : "USERNAME_EXISTS"}, status=400)

            if not email_regex.search(email):
                return JsonResponse({"MESSAGE" : "EMAIL_VALIDATION"}, status=400)

            if not password_regex.match(password):
                return JsonResponse({"MESSAGE" : "PASSWORD_VALIDATION"}, status=400)

            if not phone_regex.match(phone):
                return JsonResponse({"MESSAGE" : "PHONE_VALIDATION"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') 
                
            User.objects.create(
                name     = name, 
                email    = email, 
                phone    = phone,
                password = hashed_password, 
                username = username
            )

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)
        
        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status=400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            email       = data.get('email', None)
            phone       = data.get('phone', None)
            username    = data.get('username', None)
            password    = data.get('password', None)

            if not (email and password):
                return JsonResponse({"MESSAGE" : "EMAIl_AND_PASSWORD_REQUIRED"}, status=400)

            if not (username and password):
                return JsonResponse({"MESSAGE" : "USERNAME_AND_PASSWORD_REQUIRED"}, status=400)

            if not (phone and password):
                return JsonResponse({"MESSAGE" : "PHONE_AND_PASSWORD_REQUIRED"}, status=400)

            if len(password) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({"MESSAGE" : "PASSWORD_MUST_BE_LONGER_THAN_EIGHT_LETTERS"}, status=400)

            if User.objects.filter(Q(email=email) | Q(phone=phone) | Q(username=username)): 
                user = User.objects.get(Q(email=email) | Q(phone=phone) | Q(username=username))
                user_id = {'user' : user.id}

                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    access_token = jwt.encode(user_id , SECRET_KEY, algorithm=ALGORITHM)
                    return JsonResponse({"MESSAGE" : "SUCCESS", "TOKEN" : access_token}, status=200)

                return JsonResponse({"MESSAGE" : "UNAUTHORIZED_APPROACH"}, status=401)

            return JsonResponse({"MESSAGE" : "INVALID_USER"}, status=401)
        
        except KeyError:
        return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status=400).decode("UTF-8")

JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)