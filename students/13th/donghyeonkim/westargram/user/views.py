import re
import json

from django.db.models import Q
from django.http      import JsonResponse
from django.views     import View

from user.models      import User

class RegisterView(View):
    def post(self, request):
        user_info = json.loads(request.body)
        name      = user_info['name']
        account   = user_info['account']
        password  = user_info['password']

        if not check_account_password_key(
            account, 
            password):
            return JsonResponse(
                {'MESSAGE':'KEY_ERROR'}, status=400)

        if not account_validation(account):
            return JsonResponse(
                {'MESSAGE':'It doesn\'t fit the email or phone number format.'}, status=400)

        if not password_validation(password):
            return JsonResponse(
                {'MESSAGE':'Password must be at least 8 digits.'}, status=400)

        if account_duplicate_check(account):
            return JsonResponse(
                {'MESSAGE':'This account already exists.'}, status=400)

        if name_duplicate_check(name):
            return JsonResponse(
                {'MESSAGE':'This name already exists.'}, status=400)

        User.objects.create(
            name     = name, 
            account  = account,
            password = password)
        
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

class LoginView(View):
    def post(self, request):
        user_info = json.loads(request.body)
        account   = user_info['account']
        password  = user_info['password']

        if not check_account_password_key(
            account, 
            password):
            return JsonResponse(
                {'MESSAGE':'KEY_ERROR'}, status=400)

        if check_login(account, password):
            return JsonResponse(
                {'MESSAGE':'SUCCESS'}, status=200)
        else:
            return JsonResponse(
                {'MESSAGE':'INVALID_USER'}, status=401)

def check_account_password_key(account, password):
    if account and password:
        return True
    return False

def account_validation(account):
    if bool(
        re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', 
        account)):
        return True
    elif bool(
        re.match('^\d{3}-\d{3,4}-\d{4}$', 
        account)):
        return True
    else:
        return False

def password_validation(password):
    if len(password) >= 8:
        return True 
    return False

def account_duplicate_check(account):
    if User.objects.filter(
        Q(account=account)):
        return True
    return False

def name_duplicate_check(name):
    if User.objects.filter(
        Q(name=name)):
        return True
    return False

def check_login(account, password):
    if User.objects.filter(Q(account=account)) and (
       User.objects.filter(Q(password=password))):
       return True
    elif User.objects.filter(Q(name=account)) and (
         User.objects.filter(Q(password=password))):
        return True
    return False
    
