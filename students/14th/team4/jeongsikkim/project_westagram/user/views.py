import json
import bcrypt
import jwt

from django.views import View
from django.http import JsonResponse, HttpResponse
from django.db.models import Q


from .models import User
from core.my_settings import SECRET, ALGORITHM
from core.utils import login_decorator


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if "@" not in data["email"] or "." not in data["email"]:
                return JsonResponse({"message": "email error!"}, status=400)

            elif len(data["password"]) < 8:
                return JsonResponse({"message": "password error!"}, status=400)

            elif User.objects.filter(
                Q(user_name=data["user_name"])
                | Q(mobile_number=data["mobile_number"])
                | Q(email=data["email"])
            ):
                return JsonResponse({"message": "already in use"}, status=400)

            password = data["password"]
            hashed_password = bcrypt.hashpw(
                data["password"].encode("utf-8"), bcrypt.gensalt()
            )
            decoded_password = hashed_password.decode("utf-8")

            User.objects.create(
                user_name     = data["user_name"],
                mobile_number = data["mobile_number"],
                email         = data["email"],
                password      = decoded_password,
            )

            return JsonResponse({"message": "Sign up SUCCESS!"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KeyError!"}, status=400)


class LogInView(View):
    def post(self, request):
        data = json.loads(request.body)

        if "account" not in data:
            return JsonResponse({"message": "KeyError!"}, status=400)

        if "password" not in data:
            return JsonResponse({"message": "KeyError!"}, status=400)

        account = User.objects.filter(
            Q(user_name=data["account"])
            | Q(mobile_number=data["account"])
            | Q(email=data["account"])
        )

        if not account:
            return JsonResponse({"message": "유저 정보를 찾을 수 없습니다. 가입부터 하세요!!"}, status=401)

        password = data["password"]
        encoded_password_in_database = account.first().password.encode("utf-8")

        if bcrypt.checkpw(password.encode("utf-8"), encoded_password_in_database):

            access_token = jwt.encode(
                {"account": data["account"]},
                SECRET["secret"],
                algorithm=ALGORITHM["algorithm"],
            )
            access_token = access_token.decode("utf-8")

            return JsonResponse({"[success]access_token": access_token}, status=200)
        return JsonResponse({"message": "Wrong Password!"}, status=401)


