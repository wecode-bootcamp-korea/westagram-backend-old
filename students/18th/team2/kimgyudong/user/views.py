import json

from django.views import View
from django.http  import JsonResponse

from .models import User

class UserSignUp(View):
    def post(self, request):
        data = json.loads(request.body)
        
        if "email" not in data or "password" not in data:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        
        email    = data["email"]
        password = data["password"]

        if '@' not in email or '.' not in email:
            return JsonResponse({"message":"Put @ and . in email PLEASE."}, status = 400)
        
        if len(password) < 8:
            return JsonResponse({"message":"More than 8 letters PLEASE."}, status = 400)
        
        users = User.objects.all()
        user_list = []
        for user in users:
            user_dict = {
                'email'    : user.email,
                'password' : user.password,
            }
            user_list.append(user_dict)
        
        for user_information in user_list:
            if email == user_information['email']:
                return JsonResponse({"message":"Already posted email. Another email PLEASE."}, status = 400)
        
        for user_information in user_list:
            if password == user_information['password']:
                return JsonResponse({"message":"Already posted password. Another password PLEASE."}, status = 400)
        
        User.objects.create(email=email, password=password)
        
        return JsonResponse({'message':'SUCESS'}, status = 200)

class UserSignIn(View):
    def post(self, request):
        data = json.loads(request.body)
        if ("email" not in data) or ("password" not in data):
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)
        
        email    = data["email"]
        password = data["password"]

        users = User.objects.all()
        user_list = []
        for user in users:
            user_dict = {
                'email'    : user.email,
                'password' : user.password,
            }
            user_list.append(user_dict)
        
        user_email    = []
        user_password = []

        for user_information in user_list:
            user_email.append(user_information["email"])
            user_password.append(user_information["password"])
        
        if email in user_email:
            email_password = User.objects.get(email=email)
            if password == email_password.password:
                return JsonResponse({"message":"SUCCESS"}, status = 200)
            else:
                return JsonResponse({"message":"INVALID_USER"}, status = 401)
        else:
            return JsonResponse({"message":"INVALID_USER"}, status = 401)
        
        