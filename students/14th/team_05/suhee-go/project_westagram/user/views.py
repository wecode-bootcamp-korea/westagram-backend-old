import json
import re
import bcrypt
import jwt

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q
from django.conf      import settings

from .models          import User

class SignUpView(View):
    def post(self,request):
        data                = json.loads(request.body)

        signup_name         = data["name"]
        signup_email        = data["email"]
        signup_phone        = data["phone_number"]
        signup_password     = data["password"]

        valid_name          = re.compile(r'[a-z0-9_.]{5,30}')
        valid_email         = re.compile(r'^[a-za-z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        vaild_phone         = re.compile(r'^[0-9]*$')
        valid_password      = re.compile(r'[a-z0-9@#$]{8,12}')

        validation_name     = re.search(valid_name, signup_name)
        validation_email    = re.search(valid_email, signup_email)
        validation_phone    = re.search(vaild_phone, signup_phone)
        validation_password = re.search(valid_password, signup_password)

        try:
            # validation check
            if not validation_name :
                return JsonResponse({"messgage" : "INVAILD_NAME"}, status = 400)

            if not validation_email :
                return JsonResponse({"message":"INVAILD_EMAIL"}, status = 400)

            if not validation_phone :
                return JsonResponse({"message":"INVAILD_PHONE_NUMBER"}, status = 400)

            if not validation_password :
                return JsonResponse({"message":"INVAILD_PASSWORD"}, status = 400)

            #기존 유저와의 중복 체크 
            if User.objects.filter(
                Q(name         = signup_name) |
                Q(email        = signup_email)|
                Q(phone_number = signup_phone)
            ) :
                return JsonResponse({"message":"ALREADY_EXSIST"}, status = 400)

            # password 암호화
            hashed_password      = bcrypt.hashpw(signup_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
            name                 = signup_name,
            email                = signup_email,
            phone_number         = signup_phone,
            password             = hashed_password
            )

            return JsonResponse({"message" :"SUCCESS"}, status = 201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

class SignInView(View):
    def post(self,request):
        data            = json.loads(request.body)
        signin_name     = data["username"]
        signin_password = data["password"]

        try :
            account = User.objects.filter(
                Q(name         = signin_name)|
                Q(email        = signin_name)|
                Q(phone_number = signin_name)
            )

            if account.exists() :
                user     = account.first()
                code     = user.pk
                password = user.password

                if bcrypt.checkpw(signin_password.encode('utf-8'), password.encode('utf-8')) :
                    #token 발행
                    key       = settings.SECRET_KEY
                    algorithm = settings.ALGORITHM
                    token     = jwt.encode({"user" : code}, key, algorithm).decode('utf-8')
                    return JsonResponse({"token" : token}, status = 200)
                    return JsonResponse({"message" : "INVAILD_USER"}, status = 401)
            return JsonResponse({"message" : "INVAILD_USER"}, status = 401)

        except KeyError:
                return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
