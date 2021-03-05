import json
import re

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .models import User


class SignUpView(View):
    def post(self, request):
        
        if not request.body:
            return JsonResponse({'message': 'Empty Value'}, status=400)
        
        data = json.loads(request.body)
        
        try:
            user_name    = data['user_name']
            email        = data['email']
            password     = data['password']
            name         = data.get('name', None)
            phone_number = data.get('phone_number', None)
            
            email_match = re.match('[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]+', email)
            password_match = re.match('\S{8,}', password)
            
            if not email_match:
                return JsonResponse({'message': 'invalid email'}, status=400)

            
            if not password_match:
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
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):

        if not request.body:
            return JsonResponse({'message': 'Empty Value'}, status=400)
        
        data = json.loads(request.body)
        
        try:
            user_name     = data.get('user_name', '')
            phone_number  = data.get('phone_number', '')
            email         = data.get('email', '')
            password      = data['password']
            
            if not (user_name or phone_number or email):
                return JsonResponse({'message': 'Type at least one value'}, status=400)
            
            valid_user_id = User.objects.filter(
                Q(user_name=user_name) | Q(email=email) | Q(phone_number=phone_number)
            )
            valid_user_password = User.objects.filter(password=password)
            
            if not valid_user_id:
                return JsonResponse({'message': 'INVALID USER_ID'}, status=401)
            
            if not valid_user_password:
                return JsonResponse({'message': 'INVALID USER_PASSWORD'}, status=401)

            return JsonResponse({'message': 'SUCCSESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)