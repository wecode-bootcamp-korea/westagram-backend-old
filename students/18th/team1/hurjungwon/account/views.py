import json
import re

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .models import User


class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            user_name    = data['user_name']
            email        = data['email']
            password     = data['password']
            name         = data.get('name', None)
            phone_number = data.get('phone_number', None)
            
            email_match = re.match('[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]+', email)
            
            if not (email_match):
                return JsonResponse({'message': 'invalid email'}, status=400)

            password_match = re.match('\S{8,}', password)
            
            if not(password_match):
                return JsonResponse({'message': 'invalid password'}, status=400)

            if User.objects.filter(user_name = user_name).exists():
                return JsonResponse({'message': 'user_name already exists'}, status=400)

            User.objects.create(
                user_name    = user_name,
                email        = email,
                password     = password,
                name         = name,
                phone_number = phone_number,
            )

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        else:
            return JsonResponse({'message': 'SUCCESS'}, status=200)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            user_name     = data.get('user_name')
            phone_number  = data.get('phone_number')
            email         = data.get('email')
            password      = data['password']

            if not (user_name or phone_number or email):
                raise KeyError
            
            valid_user = User.objects.filter(
                (Q(user_name=user_name) | Q(email=email) | Q(phone_number=phone_number)) & Q(password=password)
            )

            if not valid_user:
                return JsonResponse({'message': 'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        else:
            return JsonResponse({'message': 'SUCCSESS'}, status=200)
