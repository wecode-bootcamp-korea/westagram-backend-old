import json
import re
import jwt
import bcrypt
from json.decoder import JSONDecodeError

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q 
from project_westagram.settings import SECRET_KEY

from .models          import User

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

            if not p_email.match(email):
                return JsonResponse({'message': 'INVALID_EMAIL_FORMAT'}, status=400)
            if not p_username.match(username):
                return JsonResponse({'message': 'INVALID_USERNAME_FORMAT'}, status=400)
            if not p_password.match(password):
                return JsonResponse({'message': 'INVALID_PASSWORD_FORMAT'}, status=400)
            if phone_number and not p_phone_number.match(phone_number):
                return JsonResponse({'message': 'INVALID_PHONE_NUMBER_FORMAT'}, status=400)

            # duplicate check for input
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'EXISTING_EMAIL'}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({'message': 'EXISTING_USERNAME'}, status=400)
            
            phone_number_in_db = User.objects.filter(phone_number=phone_number).first()
            if phone_number_in_db.phone_number:
                return JsonResponse({'message': 'EXISTING_PHONE_NUMBER'}, status=400)

            # hash pw and save it in str format
            hashed_pw         = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_pw = hashed_pw.decode('utf-8')
 
            User.objects.create(email=email, username=username, phone_number=phone_number, password=decoded_hashed_pw)
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

            # phone_number has unique option but `null` value is allowed.
            # so if we use None instead of False for phone_number,
            # it will match all rows that have the `null` value in phone_number column 
            username     = data.get('username', None)
            email        = data.get('email', None)
            phone_number = data.get('phone_number', False)
            password     = data['password']

            if not email and not username and not phone_number:
                return JsonResponse({'message': 'EMPTY_VALUE'}, status=400)
            
            if not password:
                return JsonResponse({'message': 'EMPTY_PASSWORD'}, status=400)
            
            user     = User.objects.filter(Q(email=email) | Q(username=username) | Q(phone_number=phone_number)).first()
            pw_in_db = user.password

            is_valid_user = bcrypt.checkpw(password.encode('utf-8'), pw_in_db.encode('utf-8'))

            if not is_valid_user:
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
            
            token = jwt.encode({'user_id': user.id}, SECRET_KEY, algorithm='HS256')
            return JsonResponse({'message': 'SUCCESS', 'token': token}, status=200)
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)
