import re
import json

from django.db.models import Q
from django.http      import JsonResponse
from django.views     import View
from user.models      import User

class RegisterView(View):
    def post(self, request):
        user_info    = json.loads(request.body)
        name         = user_info['name']
        email        = user_info['email']
        password     = user_info['password']
        phone_number = user_info['phone_number']

        if not email_password_key_check(
            email, 
            password):
            return JsonResponse(
                {'MESSAGE':'KEY_ERROR'}, status=400)

        if not email_validation(email):
            return JsonResponse(
                {'MESSAGE':'It doesn\'t fit the email format.'}, status=400)

        if not password_validation(password):
            return JsonResponse(
                {'MESSAGE':'Password must be at least 8 digits.'}, status=400)

        if email_duplicate_check(email):
            return JsonResponse(
                {'MESSAGE':'This email already exists.'}, status=400)

        if name_duplicate_check(name):
            return JsonResponse(
                {'MESSAGE':'This name already exists.'}, status=400)

        if phone_number_duplicate_check(phone_number):
            return JsonResponse(
                {'MESSAGE':'This phone number already exists.'}, status=400)

        User.objects.create(
            name         = name, 
            email        = email,
            password     = password,
            phone_number = phone_number)
        
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

def email_password_key_check(email, password):
    if email and password:
        return True
    return False

def email_validation(email):
    return bool(re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))

def password_validation(password):
    if len(password) >= 8:
        return True 
    return False

def email_duplicate_check(email):
    if User.objects.filter(Q(email=email)):
        return True
    return False

def name_duplicate_check(name):
    if User.objects.filter(Q(name=name)):
        return True
    return False   

def phone_number_duplicate_check(phone_number):
    if User.objects.filter(Q(phone_number=phone_number)):
        return True
    return False
