import json

from django.shortcuts import render
from django.http      import JsonResponse
from django.views     import View

from .models          import User

class SignUp(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            User(
                name     = data['name'],
                email    = data['email'],
                password = data['password']
            ).save()
            return JsonResponse({"message":"SUCCESS"}, status = 200)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)

    def get(self, request):
        db = User.objects.values()
        return JsonResponse({"data":list(db)}, status = 200)

class SignIn(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if data['email'] in User.objects.get(email = data['email']).email:
                user = User.objects.get(email = data['email'])
                if user.password == data['password']:
                    return JsonResponse({"message":"PASSWORD_ERROR"}, status = 201)
                else:
                    return JsonResponse({"message":"PASSWORD_ERROR"}, status = 400)
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        except Exception as content:
            return JsonResponse({"message":f"{content}"}, status = 401)
