import json
import re
from json.decoder import JSONDecodeError

from django.views     import View
from django.http      import JsonResponse
from .models          import User
from django.db.models import Q 

from utils.debugger  import debugger


class SignUpView(View):
    def post(self, request):
        try:
            data      = json.loads(request.body)

            email        = data['email']
            password     = data['password']
            username     = data['username']
            phone_number = data.get('phone_number', None)

            if not email or not password or not username:
                return JsonResponse({'message': 'EMPTY_VALUE'}, status=400)

            p_email        = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z-.]+$')
            p_password     = re.compile(r'.{8,45}')
            p_username     = re.compile(r'^[a-zA-Z0-9_-]{3,50}$')
            p_phone_number = re.compile(r'^[0-9]{3}-[0-9]{4}-[0-9]{4}$')

            # TODO : modify password validation check
            is_valid_email        = True if p_email.match(email) else False 
            is_valid_password     = True if p_password.match(password) else False
            is_valid_username     = True if p_username.match(username) else False

            if phone_number:
                is_valid_phone_number = True if p_phone_number.match(phone_number) else False
            else:
                is_valid_phone_number = True

            if not is_valid_email:
                return JsonResponse({'message': 'INVALID_EMAIL_FORMAT'}, status=400)
            if not is_valid_username:
                return JsonResponse({'message': 'INVALID_USERNAME_FORMAT'}, status=400)
            if not is_valid_password:
                return JsonResponse({'message': 'INVALID_PASSWORD_FORMAT'}, status=400)
            if not is_valid_phone_number:
                return JsonResponse({'message': 'INVALID_PHONE_NUMBER_FORMAT'}, status=400)

            # duplicate check for input
            is_existing_email = User.objects.filter(email=email).exists()
            if is_existing_email:
                return JsonResponse({'message': 'EXISTING_EMAIL'}, status=400)

            is_existing_username = User.objects.filter(username=username).exists()
            if is_existing_username:
                return JsonResponse({'message': 'EXISTING_USERNAME'}, status=400)

            is_existing_phone_number = User.objects.filter(phone_number=phone_number).exists()
            if is_existing_phone_number:
                return JsonResponse({'message': 'EXISTING_PHONE_NUMBER'}, status=400)
 
            User.objects.create(email=email, username=username, phone_number=phone_number, password=password)
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
        except:
            debugger.exception('Unexpected Error inserting user info into User Model')
            return JsonResponse({'message': 'INVALID_FORMAT'}, status=400)


class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            username     = data.get('username', None)
            email        = data.get('email', None)
            phone_number = data.get('phone_number', None)
            password     = data['password']

            if not email and not username and not phone_number:
                return JsonResponse({'message': 'EMPTY_VALUE'}, status=400)
            
            if not password:
                return JsonResponse({'message': 'EMPTY_PASSWORD'}, status=400)
            
            is_valid_account = User.objects.filter((Q(email=email) | Q(username=username) | Q(phone_number=phone_number)) & Q(password=password)).exists()
            if not is_valid_account:
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
            return JsonResponse({'message': 'SUCCESS'}, status=200)
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
