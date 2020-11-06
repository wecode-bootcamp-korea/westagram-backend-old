import json
import re

from django.shortcuts import render
from django.http      import JsonResponse
from django.views     import View

from .models import User

class Register(View):
    def post(self, request):
        data = json.loads(request.body)

        def validate_email(email):
            return bool(re.search('^[a-zA-Z0-9+-_.]+@[a-zA-Z]+\.[a-z.]+$', email))

        def validate_password(password):
            return len(password) > 5

        def validate_phone_number(phone_number):
            return bool(re.search('^[0-9]{3}-[0-9]{3,4}-[0-9]{4}$', phone_number))

        if validate_email(data['email']) == False:
            return JsonResponse({'message':'INVALID_MAIL'}, status = 400)

        if validate_password(data['password']) == False:
            return JsonResponse({'message':'INVALID_PASSWORD'}, status = 400)

        if validate_phone_number(data['phone_number']) == False:
            return JsonResponse({'meesage':'INVALID_PHONE_NUMBER'}, status = 400)

        try:
            if User.objects.filter(username = data['username']).exists():
                return JsonResponse({'message':'username already exists!'})
            elif User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message':'email already exists!'})
            elif User.objects.filter(phone_number = data['phone_number']).exists():
                return JsonResponse({'message':'phone_number already exists!'})

            User.objects.create(username = data['username'], email = data['email'], password=data['password'], phone_number = data['phone_number'])
            return JsonResponse({'message':'SUCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'meesge':'KEY_ERROR'}, status =400)

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
            return JsonResponse({'message':'INVALID_USER'}, status = 400)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)
        except UnboundLocalError:
            return JsonResponse({'message':'INVALID_USER'}, status = 400)
