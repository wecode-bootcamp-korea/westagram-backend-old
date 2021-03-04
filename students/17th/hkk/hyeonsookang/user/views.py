import json
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View
from django.db.models import Q

from my_settings import SECRET
from user.models  import User
MINIMUM_PASSWORD_LENGTH = 8

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=401)

            if User.objects.filter(Q(email=data['email']) | Q(account=data['account']) | Q(phonenumber=data['phonenumber'])).exists():
                return JsonResponse({'MESSAGE': 'ALREADY_SIGNUP'}, status=409)

            if len(data['password']) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({'MESSAGE': 'INVALID_PASSWORD'}, status=401)

            User.objects.create(
                    email      = data['email'], 
                    password   = (bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())).decode('utf-8'),
                    phonenumber= data['phonenumber'],
                    account    = data['account'],
                    )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

class LogInView(View):
    def post(self, request):
        data = json.loads(request.body)
        account = data.get('account')
        email = data.get('email')
        phonenumber = data.get('phonenumber')
        password = data.get('password')

        if not password and (email or account or phonenumber):
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

        if User.objects.filter(Q(email=email) | Q(account=account) | Q(phonenumber=phonenumber)).exists():
            id = User.objects.get(Q(email=email) | Q(account=account) | Q(phonenumber=phonenumber))

            if bcrypt.checkpw(password.encode('utf-8'),(id.password).encode('utf-8')):
                token = jwt.encode({'user_id': id.id}, SECRET, algorithm='HS256')
                return JsonResponse({'MESSAGE': 'SUCCESS', 'TOKEN': token}, status=200)
            return JsonResponse({'MESSAGE': 'CHECK_PASSWORD'}, status=404)
        return JsonResponse({'MESSAGE': 'CHECK_ID'}, status=404)

