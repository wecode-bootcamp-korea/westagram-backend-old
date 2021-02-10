import json
import bcrypt
import jwt

from django.http     import JsonResponse, HttpResponse
from django.views    import View

from user.models import User
from my_settings import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        MINIMUM_PASSWORD_LENGTH = 8
        try:
            data     = json.loads(request.body)
            name     = data['name']
            email    = data['email']
            password = data['password']
            phone    = data['phone']
        
            if name and email and password and phone:
                    
                if User.objects.filter(name=name).exists():
                    return JsonResponse({'message': 'ID_ALREADY_EXISTS'}, status=400)
                    
                if User.objects.filter(email=email).exists():
                    return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'}, status=400)

                if User.objects.filter(phone=phone).exists():
                    return JsonResponse({'message': 'PHONE_NUMBER_ALREADY_EXISTS'}, status=400)
                
                if '@' not in email or '.' not in email:
                    return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)

                if len(password) < MINIMUM_PASSWORD_LENGTH:
                    return JsonResponse({'message': 'PASSWORD_VALIDATION_ERROR'}, status=400)

                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                User.objects.create(name=name, email=email, password=hashed_password, phone=phone)

                return JsonResponse({'message': 'SUCCESS'}, status=200)
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
            user = User.objects.get(email=email)
            
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # if user.password == password:
                token = jwt.encode({'user_id': user.id}, SECRET_KEY, ALGORITHM)
                return JsonResponse({'message': 'SUCCESS', 'access_token': token}, status=200)
            return JsonResponse({'message': 'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)        




