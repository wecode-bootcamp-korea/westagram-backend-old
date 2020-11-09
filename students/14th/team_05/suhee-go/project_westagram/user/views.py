                      import json
                      import re
from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q
from .models          import User

class SignUpView(View):
    def post(self,request):
        data                = json.loads(request.body)

        signup_name         = data["name"]
        signup_email        = data["email"]
        signup_phone        = data["phone_number"]
        signup_password     = data["password"]

        valid_name          = re.compile(r'[a-z0-9_.]{5,30}')
        valid_email         = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        vaild_phone         = re.compile(r'[:digit:]')
        valid_password      = re.compile(r'[a-z0-9@#$]{8,12}')

        validation_name     = re.search(valid_name, signup_name)
        validation_email    = re.search(valid_email, signup_email)
        validation_phone    = re.search(vaild_phone, signup_phone)
        validation_password = re.search(valid_password, signup_password)

        try:

            if validation_name :
                pass
            else:
                return JsonResponse({"messgage" : "INVAILD_NAME"}, status = 400)

            if validation_email :
                pass
            else:
                return JsonResponse({"message" : "INVAILD_EMAIL"}, status = 400)

            if validation_phone :
                pass
            else:
                return JsonResponse({"message" : "INVAILD_PHONE_NUMBER"}, status = 400)

            if validation_password :
                pass
            else:
                return JsonResponse({"message" : "INVAILD_PASSWORD"}, status = 400)

            if User.objects.filter(
                Q(name         = signup_name) |
                Q(email        = signup_email)|
                Q(phone_number = signup_phone)
            ) :
                return JsonResponse({"message" : "ALREADY_EXSIST"}, status = 400)

            User.objects.create(
                name         = signup_name,
                email        = signup_email,
                phone_number = signup_phone,
                password     = signup_password
            )

            return JsonResponse({"message" : "SUCESS"}, status = 201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, statu = 400)

class SignInView(View):
    def post(self,request):
        signin_data     = json.loads(request.body)

        signin_name     = signin_data["username"]
        signin_password = signin_data["password"]

        try:
            if User.objects.filter(
                Q(name         = signin_name)|
                Q(email        = signin_name)|
                Q(phone_number = signin_name),
                password       = signin_password
            ) :
                return JsonResponse({"message":"SUCCESS"}, status = 200)

            else :
                return JsonResponse({"message" : "INVAILD_USER"}, status = 401)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

