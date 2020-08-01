import bcrypt
import json

from django.http          import JsonResponse
from django.views.generic import View

from .codes      import (
    ERROR_INVALID_INPUT,
    ERROR_INVALID_PHONE,
    ERROR_INVALID_EMAIL,
    SUCCESS_VALID_REQUEST,
)
from .models     import User
from .validators import UserRegisterValidator

class UserRegisterView(View):
    @UserRegisterValidator
    def post(self, request, **kwargs):
        phone_or_email = kwargs['phone_or_email']
        name           = kwargs['name']
        username       = kwargs['username']
        password       = kwargs['password']
        result_code    = kwargs['result_code']

        if result_code == ERROR_INVALID_INPUT:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        elif result_code == ERROR_INVALID_PHONE:
            return JsonResponse(
                {'message': 'INVALID_PHONE_NUMBER'}, 
                status = 400,
            )
        elif result_code == ERROR_INVALID_EMAIL:
            return JsonResponse({'message': 'INVALID_EMAIL'}, status = 400)
        elif result_code == SUCCESS_VALID_REQUEST:    
            has_same_phone_or_email=User.objects.filter(
                phone_or_email = phone_or_email
            )
            has_same_username = User.objects.filter(username = username)

            if has_same_phone_or_email or has_same_username:
                return JsonResponse(
                    {'message': 'ALREADY_SIGNED_UP'},
                    status=409,
                )
            else:
                bcrypted_password = bcrypt.hashpw(
                    password.encode('utf-8'), 
                    bcrypt.gensalt()
                )
                User(
                    phone_or_email=phone_or_email,
                    name=kwargs['name'],
                    username=kwargs['username'],
                    password=bcrypted_password,
                ).save()

            return JsonResponse({'message':'SUCCESS'}, status=200)

    def get(self, request):
        return JsonResponse({'hello': 'world'}, status=200)