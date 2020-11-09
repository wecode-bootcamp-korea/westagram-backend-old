import json
import re

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from user.models import User

class UsersView(View):

    def post(self, request):
        data           = json.loads(request.body)
        valid_email_re = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

        try:
            new_name     = data['name']
            new_email    = data['email']
            new_password = data['password']
            new_phone    = data['phone']
        except KeyError:
            return JsonResponse({'message': "KEY_ERROR"}, status = 400)

        #email validation
#        if '@' in new_email and '.' in new_email.split('@')[1]:
#            valid_email = True
#        else:
#            return JsonResponse({'message': "Invalid Email"}, status = 400)

        #email validation using re
        if not re.search(valid_email_re, new_email):
            valid_email = False
            return JsonResponse({'message': "Invalid Email"}, status = 400)
        else:
            valid_email = True

        #password validation
        if not len(new_password) >= 8:
            valid_password = False
            return JsonResponse({'message': "Invalid Password"}, status = 400)
        else:
            valid_password = True

        #duplacted value validation
        exist_user = User.objects.filter(Q(name=new_name) | Q(phone=new_phone) | Q(email=new_email))
        if not exist_user:
            valid_user = True
        else:
            return JsonResponse({'message': "Name, Phone or Email is already exists"}, status = 400)

        if valid_email and valid_password and valid_user:
            user = User.objects.create(
                name     = new_name,
                email    = new_email,
                phone    = new_phone,
                password = new_password,
            )

        return JsonResponse({'message': "SUCCESS"}, status = 200)

class LoginView(View):

    def post(self, request):
        data           = json.loads(request.body)
        is_phone       = False
        is_email       = False
        is_name        = False
        valid_email_re = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

        try:
            input_account  = data['account']
            input_password = data['password']
        except Exception as error_msg:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

        if re.search(valid_email_re, input_account):
            is_email = True
        elif input_account.isdigit():
            is_phone = True
        else:
            is_name = True

        try:
            user = User.objects.get(Q(name=input_account)|Q(email=input_account)|Q(phone=input_account))
        except Exception:
            return JsonResponse({'message': 'INVALID_USER'}, status = 400)

        if input_password == user.password:
            return JsonResponse({'message': 'SUCCESS'}, status = 200)

        return JsonResponse({'message': 'INVALID PASSWORD OR ACCOUNT'}, status = 400)
