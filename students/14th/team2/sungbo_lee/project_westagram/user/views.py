import json
from django.views import View
from django.http import JsonResponse
from user.models import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            user = User(
            email        = data["email"],
            password     = data["password"],
            phone_number = data["phone_number"],
            name         = data["name"],
            )

            if '@' not in user.email:
                raise KeyError("error")

            if '.' not in user.email:
                raise KeyError("error")

            if len(user.password) < 8:
                raise KeyError("error")

            if User.objects.filter(email=user.email):
                raise KeyError("error")

            if User.objects.filter(phone_number=user.phone_number):
                raise KeyError("error")

            if User.objects.filter(name=user.name):
                raise KeyError("error")

            user.save()

            return JsonResponse({"message":"SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)

    def get(self, request):

        return JsonResponse({"Hello":"World"}, status=200)

class LogInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            email        = data["email"]
            password     = data["password"]
            phone_number = data["phone_number"]
            name         = data["name"]

            if not User.objects.get(name=data["name"]):
                raise Exception("error")
            if not User.objects.get(name=data["name"], password=data["password"]):
                raise Exception("error")

            return JsonResponse({"message":"SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)

        except Exception:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)

    def get(self, request):

        return JsonResponse({"Hello":"World"}, status=200)
