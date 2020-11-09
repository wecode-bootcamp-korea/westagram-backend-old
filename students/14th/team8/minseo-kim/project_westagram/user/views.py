import json
import re
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import User


class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_data = {
                'name': data['name'],
                'email': data['email'],
                'password': data['password'],
                'number': data['number']
            }

            email_validation = re.compile(
                r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            if len(user_data['password']) < 8:
                return JsonResponse(
                    {'message':'PASSWORD_VALIDATION'}, status=400
                )

            if not re.match(email_validation, user_data['email']):
                return JsonResponse(
                    {'message':'EMAIL_VALIDATION'}, status=400
                    )

            if User.objects.filter(name=user_data['name']):
                return JsonResponse(
                    {'message':'INVALID_NAME'},status=400)
            
            if User.objects.filter(email=user_data['email']):
                return JsonResponse(
                    {'message':'INVALID_EMAIL'},status=400)
            if User.objects.filter(number=user_data['number']):
                return JsonResponse(
                    {'message':'INVALID_NUMBER'}, status=400)
                
            User.objects.create(
                name=user_data['name'],
                email=user_data['email'],
                password=user_data['password'],
                number=user_data['number']
            )

            return JsonResponse({'message':'SUCCESS'},status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class SigninView(View):
    def post(self, request):
        try:
            signin_data = json.loads(request.body)

            if User.objects.filter(email=signin_data['email']).exists():
                user = User.objects.get(email=signin_data['email'])
                if user.password == signin_data['password']:
                    return JsonResponse({'message':'LOGIN_SUCCESS'},status=200)
                else:
                    return JsonResponse({'message':'WRONG_PASSWORD'},status=400)
            else:
                return JsonResponse({'message':'NOT_EXIST_USER'},status=400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)

