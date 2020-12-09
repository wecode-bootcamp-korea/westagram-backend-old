import json
import bcrypt
import jwt

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q

from westagram.settings import SECRET_KEY
from .models            import User


class SignUpView(View):
    def post(self, request):
        try:
            data                 = json.loads(request.body)
            data['username']     = data.get('username')
            data['email']        = data.get('email')
            data['phone_number'] = data.get('phone_number')
            minimum_password     = 8

            if User.objects.filter(Q(username=data['username']) & Q(email=data['email']) & Q(phone_number=data['phone_number'])).exists():
                return JsonResponse({'message': 'USER_ALREADY_EXISTS'}, status = 400)

            if data['email'] is not None and ('@' not in data['email'] or '.' not in data['email']):
                return JsonResponse({'message': 'WRONG_FORM'}, status = 400)

            if len(data['password']) < minimum_password:
                return JsonResponse({'message': 'TOO_SHORT_PASSWORD'}, status = 400)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt())

            User(
                username        = data['username'],
                email           = data['email'],
                phone_number    = data['phone_number'],
                password        = hashed_password.decode('utf-8'),
            ).save()
            return JsonResponse({'message': 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        data                 = json.loads(request.body)
        data['username']     = data.get('username')
        data['email']        = data.get('email')
        data['phone_number'] = data.get('phone_number')

        try:
        #    if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        #        token = jwt.encode({'username' : data['username']}, SECRET_KEY, algorithm = "HS256")
        #        token = token.decode('utf-8')

            if data['username'] is not None:
                if User.objects.filter(username=data['username']).exists():
                    user = User.objects.get(username=data['username'])
                    if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                        token = jwt.encode({'username' : data['username']}, SECRET_KEY, algorithm = "HS256")
                        token = token.decode('utf-8')
                        return JsonResponse({'message': 'SUCCESS'}, status = 200)
                    elif user.password != data['password']:
                       return JsonResponse({'message': 'INVALID_USER'}, status = 400)

            if data['email'] is not None:
                if User.objects.filter(email=data['email']).exists():
                    user = User.objects.get(email=data['email'])
                    if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                        token = jwt.encode({'email' : data['email']}, SECRET_KEY, algorithm = "HS256")
                        token = token.decode('utf-8')
                        return JsonResponse({'message': 'SUCCESS'}, status = 200)
                    elif user.password != data['password']:
                        return JsonResponse({'message': 'INVALID_USER'}, status = 400)

            if data['phone_number']is not None:
                if User.objects.filter(phone_number=data['phone_number']).exists():
                    user = User.objects.get(phone_number=data['phone_number'])
                    if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                        token = jwt.encode({'phone_number' : data['phone_number']}, SECRET_KEY, algorithm = "HS256")
                        token = token.decode('utf-8')
                        return JsonResponse({'message': 'SUCCESS'}, status = 200)
                    elif user.password != data['password']:
                        return JsonResponse({'message': 'INVALID_USER'}, status = 400)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
