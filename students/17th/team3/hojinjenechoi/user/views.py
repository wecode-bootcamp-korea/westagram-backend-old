import json
import bcrypt
import jwt
import re
import my_settings

from django.views      import View
from django.http       import JsonResponse
from django.db.models  import Q

from user.models    import User

MINIMUM_PASSWORD_LENGTH = 8

email_regex = re.compile(r'.*[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+.*')
phone_regex = re.compile(r'^\d{3}-\d{4}-\d{4}$')
password_regex = re.compile(r'[A-Za-z0-9@#$%^&+=]{8,}')

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email    = data['email']
            phone    = data['phone']
            nickname = data['nickname']
            password = data['password']

            if not email_regex.match(email): 
                return JsonResponse({'message':'INVALID_EMAIL'}, status=400)
            
            if not phone_regex.match(phone):  
                return JsonResponse({'message':'INVALID_PHONE'}, status=400)
            
            if not password_regex.match(password):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)

            if User.objects.filter(Q(email=email) | Q(phone=phone)).exists():
                return JsonResponse({'message':'USER_ALREADY_EXISTS'}, status=409)
            
            if User.objects.filter(nickname=nickname).exists():
                return JsonResponse({'message':'NICKNAME_ALREADY_EXISTS'}, status=409)

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
        try: 
            data = json.loads(request.body)

            email    = data.get('email', None)
            phone    = data.get('phone', None)
            nickname = data.get('nickname', None)
            password = data['password']
            
            if User.objects.filter(Q(email=email) | Q(phone=phone) | Q(nickname=nickname)).exists():
                user = User.objects.get(Q(email=email) | Q(phone=phone)| Q(nickname=nickname))

                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    token = jwt.encode({'email' : user.email}, my_settings.SECRET_KEY, my_settings.ALGORITHM)               
                    return JsonResponse({'message': 'SUCCESS','token' : token}, status=200)    
                    
            return JsonResponse({'message':'INVALID_USER'},status=401)    
            
        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

##
# http -v POST 127.0.0.1:8000/user/signin email='jene0000@gmail.com'nickname='jene0000' password='00000000' phone='00011112222'
