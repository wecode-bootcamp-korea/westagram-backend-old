import json
import bcrypt

from django.http  import JsonResponse
from django.views import View

from user.models  import User
MINIMUM_PASSWORD_LENGTH = 8

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=401)

            if User.objects.filter(email=data['email']).exists() or User.objects.filter(phonenumber=data['phone_number']).exists() or User.objects.filter(email=data['account']).exists():
                return JsonResponse({'MESSAGE': 'ALREADY_SIGNUP'}, status=409)

            if len(data['password']) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({'MESSAGE': 'INVALID_PASSWORD'}, status=401)

            User.objects.create(
                    email      = data['email'], 
                    password   = (bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())).decode('utf-8'),
                    phonenumber= data['phone_number'],
                    account    = data['account'],
                    )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

class LogInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        
            if User.objects.filter(email=data['email']).exists() or User.objects.filter(account='account').exists() or User.objects.filter(phonenumber='phone_number').exists():
                id = User.objects.get(email=data['email']) or User.objects.get(account='account') or User.objects.get(phonenumber='phone_number')

                if bcrypt.checkpw(data['password'].encode('utf-8'),(id.password).encode('utf-8')) == True:
                    return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)
                else:
                    return JsonResponse({'MESSAGE': 'CHECK_PASSWORD'}, status=404)
            else:
                return JsonResponse({'MESSAGE': 'CHECK_ID'}, status=404)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)
