import json, bcrypt, jwt, re

from django.views   import View
from django.http    import JsonResponse, HttpResponse

from .models        import User
from my_settings    import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email        = data['email']
            password     = data['password']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message' : 'ALREADY_EXISTS'}, status = 400)

            regex_email    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
            regex_password = '\S{8,25}'
            if not re.match(regex_email, email):
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)
            if not re.match(regex_password, password):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)

            password       = data['password'].encode('utf-8')
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

            User.objects.create(email=email, password=password_crypt)
            return JsonResponse({'message': 'SUCCESS!'}, status=201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            user = User.objects.get(email = data['email'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID_USER'}, status=400)

            token = jwt.encode({ 'password' : data['password'] }, SECRET_KEY, algorithm='HS256')
            return JsonResponse({'message' : 'WOW!!!!SUCCESS!!!!', 'access_token' : token.decode('utf-8')}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)