import json

from django.http import JsonResponse
from django.views import View
from django.db.models import Q 

from .models import User

MININUM_PASSWORD_LENGTH = 8


class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            mobile_number = data['mobile_number']
            email         = data['email']
            full_name     = data['full_name']
            username      = data['username']
            password      = data['password']

            if mobile_number is None and email is None:
                return JsonResponse(
                    {'message': 'INVALID_INPUT'}, 
                    status=400
                )

            if email is not None:
                if '@' not in email or '.' not in email:
                    return JsonResponse(
                        {'message': 'INVALID_EMAIL'}, 
                        status=400
                    )
            
            if len(password) < MININUM_PASSWORD_LENGTH:
                return JsonResponse(
                    {'message': 'INVALID_PASSWORD'},
                    status=400
                )
            
            if mobile_number is not None and User.objects.filter(mobile_number=mobile_number).exists():
                return JsonResponse(
                    {'message': 'NUMBER_ALREADY_EXISTS'},
                    status=400
                )

            if email is not None and User.objects.filter(email=email).exists():
                return JsonResponse(
                    {'message': 'EMAIL_ALREADY_EXISTS'},
                    status=400
                )
        
            if User.objects.filter(username=username).exists():
                return JsonResponse(
                    {'message': 'USERNAME_ALREADY_EXISTS'},
                    status=400
                )


            User.objects.create(
                mobile_number = mobile_number,
                email = email,
                password = password,
                full_name= full_name,
                username= username
            )


            return JsonResponse(
                {'message': 'SUCCESS'},
                status=200
            )


        except KeyError:
            return JsonResponse(
                {'message': 'KEY_ERROR'},
                status=400
            )


class LoginView(View):
    def post(self, request):
            data = json.loads(request.body)

            try:
                    username = data.get('username', None)
                    password = data['password']
                    mobile_number = data.get('mobile_number', None)
                    email = data.get('email', None)

                    if User.objects.filter(Q(username=username) | Q(mobile_number=mobile_number) | Q(email=email)).exists():
                        if User.objects.get(Q(username=username) | Q(mobile_number=mobile_number) | Q(email=email)).password == password:
                            return JsonResponse({'message': 'LOGIN_SUCCESS'}, status=200)
                        else:
                            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

                    else:
                        return JsonResponse({"message": "USER_NOT_FOUND"}, status=400)

            except:
                    return JsonResponse({"message": "KEY_ERROR"}, status=400)
