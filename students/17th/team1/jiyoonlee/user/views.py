import json

from django.http import JsonResponse
from django.views import View

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
            
            if mobile_number is not None and User.objects.filter(mobile_number=data['mobile_number']).exists():
                return JsonResponse(
                    {'message': 'NUMBER_ALREADY_EXISTS'},
                    status=400
                )

            if email is not None and User.objects.filter(email=data['email']).exists():
                return JsonResponse(
                    {'message': 'EMAIL_ALREADY_EXISTS'},
                    status=400
                )

            if User.objects.filter(username=data['username']).exists():
                return JsonResponse(
                    {'message': 'USERNAME_ALREADY_EXISTS'},
                    status=400
                )


            User.objects.create(
                mobile_number = data['mobile_number'],
                email = data['email'],
                password = data['password'],
                full_name= data['full_name'],
                username= data['username']
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
