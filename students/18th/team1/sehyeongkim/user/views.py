import json
import re
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View

from user.models import User
from my_settings import SECRET_KEY

class SignUpView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            user_email    = data['email']
            user_password = data['password']

            if len(user_password) < 8:
                return JsonResponse({'message': 'Password is too short'}, status = 400)
            
            p = re.compile("^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-z]+$")
            if not p.match(user_email):
                return JsonResponse({'message': 'Check your email'}, status = 400)
            
            if User.objects.filter(email = user_email).exists():
                return JsonResponse({'message': 'User already exists'}, status = 400)

            hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
            password        = hashed_password.decode('utf-8')
            User.objects.create(email = user_email, password = password)
            return JsonResponse({'message': 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status = 500)

class LoginView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            user_email    = data['email']
            user_password = data['password']

            user_info = User.objects.get(email = user_email)
            
            if bcrypt.checkpw(user_password.encode('utf-8'), user_info.password.encode('utf-8')):
                access_token = jwt.encode({'user_id': user_info.id}, SECRET_KEY, algorithm = 'HS256')
                return JsonResponse({'message': 'SUCCESS', 'access_token': access_token}, status = 200)

        except KeyError:
           return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status = 400)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status = 500)
