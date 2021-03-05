import json
import re

from django.http  import JsonResponse
from django.views import View

from user.models import User

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

            User.objects.create(email = user_email, password = user_password)
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

            if User.objects.filter(email = user_email).exists() == False or User.objects.filter(password = user_password).exists() == False:
                return JsonResponse({'message': 'INVALID_USER'}, status = 400)

            return JsonResponse({'message': 'SUCCESS'}, status = 400)
           
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status = 500)

