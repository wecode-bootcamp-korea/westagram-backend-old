import json, bcrypt, jwt, re

from django.views   import View
from django.http    import JsonResponse, HttpResponse

from .models        import User
from my_settings    import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        email        = data['email']
        password     = data['password']

        if not data['email']:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        elif not data['password']:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

        if User.objects.filter(email=email):
            return JsonResponse({'message' : 'Already Exists'}, status = 400)

        regex_email    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
        regex_password = '\S{8,25}'
        if not re.match(regex_email, email):
            return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)
        elif not re.match(regex_password, password):
            return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)

        password       = data['password'].encode('utf-8')
        password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())
        password_crypt = password_crypt.decode('utf-8')

        User.objects.create(email=email, password=password_crypt)
        return JsonResponse({'message': 'SUCCESS!'}, status=200)


class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if User.objects.get(email = data['email']):
                user = User.objects.get(email = data['email'])

            if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({ 'password' : data['password'] }, SECRET_KEY, algorithm='HS256')
            
            else:
                return JsonResponse({'message' : 'INVALID_USER'}, status=400)

            return JsonResponse({'message' : 'WOW!!!!SUCCESS!!!!', 'access_token' : token.decode('utf-8')}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status=401)