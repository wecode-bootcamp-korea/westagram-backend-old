import json

from django.views import View
from django.http  import JsonResponse, HttpResponse

from .models      import Users

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Users.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "EXISTS_EMAIL"}, status=400)

            if Users.objects.filter(phone_number=data['phone_number']).exists():
                return JsonResponse({"message": "EXISTS_PHONE_NUMBER"}, status=400)

            if not data['email'] or not data['password']:
                return JsonResponse({"message": "KEY_ERROR"}, status=400)

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

            Users.objects.create(
                name         = data["name"],
                phone_number = data["phone_number"],
                email        = data["email"],
                password     = data["password"],
            )
            return JsonResponse({"message": "SUCCESS"}, status = 200)

        except:
            return JsonResponse({"message": "INVALID_ERROR"}, status = 400)

    def get(self, request):
        user_data = Users.objects.values()
        return JsonResponse({"users":list(user_data)}, status = 200)

