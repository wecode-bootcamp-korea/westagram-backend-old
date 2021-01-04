import json, re

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q
from .models          import User


class SignUpView(View):
    def post(self, request):
        data                = json.loads(request.body)
        # 이메일은 숫자나 특수문자로 시작하면 안된다.
        pattern             = re.compile(r"[^0-9\W]\w+@[a-zA-Z]+\.[a-zA-Z]+", re.I)
        MIN_LENGTH_PASSWORD = 8

        try:
            name         = data["name"]
            email        = data["email"]
            phone_number = data["phone_number"]
            password     = data["password"]

            if User.objects.filter(
                Q(name=name) and Q(email=email) and Q(phone_number=phone_number)
            ).exists():
                return JsonResponse(
                    {"message": "USER_{}_EXIST_SIGN_IN".format(name)}, status=400
                )

            if not pattern.match(email):
                return JsonResponse({"message": "NOT_PROPER_EMAIL"}, status=400)

            if len(password) < MIN_LENGTH_PASSWORD:
                return JsonResponse(
                    {"message": "AT_LEAST_{}_PASSOWRD".format(MIN_LENGTH_PASSWORD)}
                )

            if User.objects.filter(
                Q(name=name) | Q(email=email) | Q(phone_number=phone_number)
            ).exists():
                return JsonResponse({"message": "SAME_INFO_ENTERED"}, status=400)

            # if User.objects.filter(name=name).exists():
            #     return JsonResponse({
            #             "message": "SAME_NAME_EXIST"
            #         }, status=400)

            # if User.objects.filter(email=email).exists():
            #     return JsonResponse({
            #                 "message": "SAME_EMAIL_EXIST"
            #             }, status=400)

            # if User.objects.filter(phone_number=phone_number).exists():
            #     return JsonResponse({
            #         "message": "SAME_PHONE_NUMBER_EXIST"
            #     })

            User.objects.create(
                name         = name,
                email        = email,
                phone_number = phone_number,
                password     = password,
            )

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError as e:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        data = list(data.values())

        try:
            id_for_login = data[0]
            password     = data[1]

            user = User.objects.filter(
                  Q(name=id_for_login)
                | Q(email=id_for_login)
                | Q(phone_number=id_for_login)
            )

            if not user.exists():
                return JsonResponse({"message": "INVALID_USER_SIGN_UP"}, status=401)

            if user.exists():
                if password != user[0].password:
                    return JsonResponse({"message": "INVALID_USER"}, status=401)
                else:
                    return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
