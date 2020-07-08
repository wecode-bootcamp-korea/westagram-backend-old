from django.shortcuts import render
import json
from django.views import View
from django.http import JsonResponse
from .models import User

class signUp(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            User(
                    name = data['name'],
                    email = data['email'],
                    password = data['password']
                    ).save()
        except Exception as e:
            return JsonResponse({"message": f"{e}"}, status=400)

        return JsonResponse({'message':'SUCCESS'}, status=200)
    def get(self, request):
        user_data = user.objects.values()
        return JsonResponse({'user':list(user_data)}, status=200)

class signIn(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            i = data['name']
            p = data['password']

            if (User.objects.get(name=i)):
                if (User.objects.get(password=p)):
                    return JsonResponse({'message':'SUCCESS'}, status=200)

        except Exception as e:
            return JsonResponse({"message": f"{e}"}, status=401)
