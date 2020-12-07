import re
import json
from django.http import JsonResponse

from django.views import View
from user.models import User

validation = {'email':'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,4}))', 
              'password':'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
              'phonenumber':'/01[01789]\d{3,4}\d{4}/'
             }


class SignUp(View):

    def post(self, request):
        data = json.loads(request.body)
        
        data_email       = data['email']
        data_name        = data['name']
        data_phonenumber = data['phonenumber']
        data_password    = data['password']
        
        account_type_list = [data_email, data_name, data_phonenumber]

        if not ((data_email or data_name or data_phonenumber) and data_password):
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
       
        if data_email and not re.match(validation['email'], data_email):
            return JsonResponse({"message": "EMAIL_INVALIDATION"}, status = 400)

        if not re.match(validation['password'], data_password):
            return JsonResponse({"message": "PASSWORD_INVALIDATION"}, status = 400)

        for account_type_checker in account_type_list:
            if account_type_checker:
                if User.objects.filter(account = account_type_checker).exists():
                    return JsonResponse({"message": "ALREADY_EXISTS_ACCOUNT"}, status = 400)
                else:
                    user = User.objects.create(account = account_type_checker, password = data_password)   
                    break
        return JsonResponse({"message": "SUCCESS"}, status = 201)

class SignIn(View):
    def post(self, request):
        users         = User.objects.all()
        data          = json.loads(request.body)

        data_account  = data['account']
        data_password = data['password']
        
        if not (data_account and data_password):
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)

        if User.objects.filter(account = data_account, password = data_password).exists():
            return JsonResponse({"message": "SUCCESS"}, status = 200)
        else:
            return JsonResponse({"message": "INVALID_USER"}, status = 401)



