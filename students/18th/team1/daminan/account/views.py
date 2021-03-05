import json

from django.views import View
from django.http  import JsonResponse

from .models import User

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({"message": "EMAIL_ERROR"}, status=400)
            if User.objects.filter(password=data['password']).exists():
                return JsonResponse({"message": "PASSOWRD_ERROR"}, status=400)
            if '@' in data['email'] and '.' in data['email'] and len(data['password']) >= 8:
                user     = User.objects.create(
                email    = data['email'],
                password = data['password']
            )
                return JsonResponse({"message": "SUCCESS"}, status=200)
            return JsonResponse({"message":"MAKE_FAIL"}, status=400)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
   

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.all().filter(email=data['email'], password=data['password']).exists() == True:
                return JsonResponse({"message":"SUCCESS"}, status=200)
            else:
                return JsonResponse({"message":"INVALID_USER"}, status=401)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)