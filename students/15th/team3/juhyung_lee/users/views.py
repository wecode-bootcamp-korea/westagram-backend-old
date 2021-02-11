import json
import bcrypt
import jwt

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q

from my_settings        import SECRET_KEY, ALGORITHM
from .models            import User


class SignUpView(View):
    def post(self, request):
        try:
            data                = json.loads(request.body)
            username            = data.get('username')
            email               = data.get('email')
            phone_number        = data.get('phone_number')
            password            = data['password']
            MIN_PASSWORD_LENGTH = 8

            if User.objects.filter(username = username, email = email, phone_number = phone_number).exists():
                return JsonResponse({'message': 'USER_ALREADY_EXISTS'}, status = 400)

            if email and ('@' not in email or '.' not in email):
                return JsonResponse({'message': 'WRONG_FORM'}, status = 400)

            if len(password) < MIN_PASSWORD_LENGTH:
                return JsonResponse({'message': 'TOO_SHORT_PASSWORD'}, status = 400)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt())

            User(
                username        = username,
                email           = email,
                phone_number    = phone_number,
                password        = hashed_password.decode('utf-8'),
            ).save()
            return JsonResponse({'message': 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

class SignInView(View):
    def post(self, request):
        data         = json.loads(request.body)
        username     = data.get('username')
        email        = data.get('email')
        phone_number = data.get('phone_number')
        password     = data['password']

        try:
            if User.objects.filter(username = username, email = email, phone_number = phone_number).exists():
                user = User.objects.get(username = username, email = email, phone_number = phone_number)
                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'username': username, 'email': email, 'phone_number': phone_number}, SECRET_KEY, algorithm = ALGORITHM)
                    return JsonResponse({'message': 'SUCCESS', 'token': token.decode('utf-8')}, status = 200)
                else:
                    return JsonResponse({'message': 'INVALID_USER'}, status = 401)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)


