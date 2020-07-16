import json, bcrypt, jwt

from django.shortcuts import render
from django.http      import JsonResponse
from django.views     import View

from .models          import User
from mysite.settings  import SECRET_KEY

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            User(
                email    = data['email'],
                password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            ).save()
            return JsonResponse({"message":"SUCCESS"}, status = 200)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)

    def get(self, request):
        db = User.objects.values()
        return JsonResponse({"data":list(db)}, status = 200)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email = data['email']).exists():
                user = User.objects.get(email = data['email'])
                if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                    return JsonResponse({"message":"SUCCESS"}, status = 200)
                else:
                    return JsonResponse({"message":"PASSWORD_ERROR"}, status = 400)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        except Exception as e:
            return JsonResponse({"message":f"{e}"}, status = 400)
