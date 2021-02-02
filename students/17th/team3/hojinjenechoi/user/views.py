import json
import bcrypt
import jwt
import my_settings

from django.views      import View
from django.http       import JsonResponse
from django.db.models  import Q

from user.models    import User

MINIMUM_PASSWORD_LENGTH = 8

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        email    = data['email']
        phone    = data['phone']
        nickname = data['nickname']
        password = data['password']

        try:
            if '@' not in email or '.' not in email:
              return JsonResponse({'message':'INVALID_EMAIL'}, status=400)

            if User.objects.filter(Q(email=email) | Q(phone=phone)).exists():
                return JsonResponse({'message':'USER_ALREADY_EXISTS'}, status=409)
            
            if User.objects.filter(nickname=nickname).exists():
                return JsonResponse({'message':'NICKNAME_ALREADY_EXISTS'}, status=409)

            if len(password) < MINIMUM_PASSWORD_LENGTH :
                return JsonResponse({'message':'SHORT_PASSWORD'}, status=400)

            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                email    = email,
                password = hashed_pw,
                nickname = nickname,
                phone    = phone
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

    def get(self, request):
        user = User.objects.values()
        return JsonResponse({'message':list(user)}, status=200)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        email    = data.get('email', None)
        phone    = data.get('phone', None)
        nickname = data.get('nickname', None)
        password = data.get('password', None)

        try: 
            if User.objects.filter(Q(email=email) | Q(phone=phone)).exists():
                user = User.objects.get(Q(email=email) | Q(phone=phone))

                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'email' : data['email']}, my_settings.SECRET_KEY, algorithm = 'HS256')                     
                    return JsonResponse({'message': 'SUCCESS','token' : token }, status=200)    
                    
                return JsonResponse({'MESSAGE':'INVALID_USER'},status=401)    
            
        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400)