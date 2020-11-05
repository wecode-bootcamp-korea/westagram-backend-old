import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import User

class SignIn(View):
    def get(self, request):
        return JsonResponse({'message':'bless'}, status=200)

    def post(self, request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(username = data['username']).exists():
                return JsonResponse({'message':'username already exists!'})
            elif User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message':'email already exists!'})
            elif User.objects.filter(email = data['phone_number']).exists():
                return JsonResponse({'message':'phone_number already exists!'})

            User.objects.create(username = data['username'], email = data['email'], password=data['password'], phone_number = data['phone_number'])
            return JsonResponse({'message':'SUCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'meesge': 'KEY_ERROR'}, status =400)

class LogIn(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(username = data['key']).exists():
                user = User.objects.get(username = data['key'])
            elif User.objects.filter(email = data['key']).exists():
                user = User.objects.get(email = data['key'])
            elif User.objects.filter(phone_number = data['key']).exists():
                user = User.objects.get(phone_number = data['key'])
                print(user.password)
            if user.password == data['password']:
                return JsonResponse({'message':'SUCESS'}, status  = 200)
            return JsonResponse({'message': 'INVALID_USER'}, status = 400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

