import json
import re

from django.views    import View
from django.http     import JsonResponse
from .models         import User
from utils.debugger  import debugger


class SignUpView(View):
    def post(self, request):
        # 예외 처리
        data      = request.body
        json_data = json.loads(data)

        try:
            email    = json_data['email']
            password = json_data['password']
            
            if not email or not password:
                return JsonResponse({'message': 'EMPTY_VALUE'}, status=400)

            p_email    = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z-.]+$')
            p_password = re.compile(r'.{8,45}')

            # TODO : modify password validation check
            is_valid_email    = True if p_email.match(email) else False 
            is_valid_password = True if p_password.match(password) else False

            if not is_valid_email or not is_valid_password:
                return JsonResponse({'message': 'INVALID_FORMAT'}, status=400)

            is_existing_user = User.objects.filter(email=email).exists()
            if is_existing_user:
                return JsonResponse({'message': 'EXISTING_USER'}, status=400)

            User.objects.create(email=email, password=password)

        except KeyError:
            debugger.exception('KeyError')
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except:
            debugger.debug('Unexpected Error inserting user info into User Model')
            return JsonResponse({'message': 'INVALID_FORMAT'}, status=400)
        return JsonResponse({'message': 'SUCCESS'}, status=200)


class LoginView(View):
    def post(self, request):
        data      = request.body
        json_data = json.loads(data)

        try:
            email    = json_data['email']
            password = json_data['password']
        except KeyError:
            debugger.exception('KeyError')
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        if not email or not password:
            return JsonResponse({'message': 'EMPTY_VALUE'}, status=400)
        
        is_valid_account = User.objects.filter(email=email, password=password).exists()
        if not is_valid_account:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)
        return JsonResponse({'message': 'SUCCESS'}, status=200)
