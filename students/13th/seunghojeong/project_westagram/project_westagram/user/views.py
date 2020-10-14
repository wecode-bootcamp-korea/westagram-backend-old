import json
import bcrypt
import jwt

from django.views import View
from django.http  import JsonResponse, HttpResponse

from .models      import Users

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Users.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "EXISTS_EMAIL"}, status=400)

#           if Users.objects.filter(phone_number=data['phone_number']).exists():
#               return JsonResponse({"message": "EXISTS_PHONE_NUMBER"}, status=400)

            if len(data['password']) < 8:
                return JsonResponse({"message": "PW_IS_TOO_SHORT"}, status=400)

            if '@' not in str(data['email']) or '.' not in str(data['email']):
                return JsonResponse({"message": "NOT_IN_EMAIL_FORM"}, status=400)

#           Users(
#               name         = data["name"],
#               phone_number = data["phone_number"],
#               email        = data["email"],
#               password     = data["password"],
#               ).save()
            hashed_pw = bcrypt.hashpw(
                data["password"].encode("UTF-8"), bcrypt.gensalt()
            )

            Users.objects.create(
            #    name         = data["name"],
            #    phone_number = data["phone_number"],
                email        = data["email"],
                password     = hashed_pw.decode("UTF-8")
            )
            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    def get(self, request):
        user_data = Users.objects.values()
        return JsonResponse({"users":list(user_data)}, status=200)

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        print(data)

        try:
            email_from_fe = data["email"]
            pw_from_fe    = data["password"]


            if Users.objects.filter(email=email_from_fe).exists():
                user = Users.objects.get(email=email_from_fe)

                if bcrypt.checkpw(pw_from_fe.encode("UTF-8"), user.password.encode("UTF-8")):
                    token = jwt.encode({"email": email_from_fe}, "SECRET_KEY", algorithm = "HS256")
                    token = token.decode("UTF-8")

                    return JsonResponse({"message": "SUCCESS"}, status=200)
#                   return JsonResponse({"token": token}, status=200)

                return JsonResponse({"message": "INVALID_ERROR(WRONG_PW)"}, status=401)

            return JsonResponse({"message": "INVALID_ERRPR(DOESNT EXIST ACCOUNT)"}, status=401)

        except KeyError:
            return JsonResponse({"messsage": "KEY_ERROR(ID OR PW MISSING)"}, status=400)
