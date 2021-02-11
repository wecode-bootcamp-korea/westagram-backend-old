import json
import re
import bcrypt
import jwt
from django.views import View
from django.http import JsonResponse
from .models import User

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            email_validation = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            if len(data['password']) < 8:
                return JsonResponse({'message':'PASSWORD_VALIDATION'}, status=400)

            if not re.match(email_validation,data['email']):
                return JsonResponse({'message':'EMAIL_VALIDATION'}, status=400)

            if User.objects.filter(name=data['name']):
                return JsonResponse({'message':'INVALID_NAME'},status=400)

            if User.objects.filter(email=data['email']):
                return JsonResponse({'message':'INVALID_EMAIL'},status=400)

            if User.objects.filter(number=data['number']):
                return JsonResponse({'message':'INVALID_NUMBER'}, status=400)

            User.objects.create(
                name     = data['name'],
                email    = data['email'],
                password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt()).decode('utf-8'),
                number   = data['number']
            )

            return JsonResponse({'message':'SIGN_UP_SUCCESS'},status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class SigninView(View):
    def post(self, request):
        try:
            signin_data = json.loads(request.body)

            if User.objects.filter(email=signin_data['email']).exists():
                user = User.objects.get(email=signin_data['email'])
                SECRET_KEY = '0_i-v1!p2f4c5hq^46_!3vq-m1clee%edh-x17u)%dl!tfg9tl'

                if bcrypt.checkpw(signin_data['password'].encode('utf-8'),user.password.encode('utf-8')):
                    access_token = jwt.encode({'id': user.id},SECRET_KEY,algorithm='HS256')                     
                    return JsonResponse({'message':'LOGIN_SUCCESS','token': access_token.decode('utf-8')},status=200)
                else:
                    return JsonResponse({'message':'WRONG_PASSWORD'},status=400)

            return JsonResponse({'message':'NOT_EXIST_USER'},status=400)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)


