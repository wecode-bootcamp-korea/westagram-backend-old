import json, re, traceback, bcrypt, jwt

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Q
from django.core.exceptions import ValidationError

from .models                import User
from my_settings            import SECRET

MINIMUM_PASSWORD_LENGTH = 8

def validate_email(email):
    pattern = re.compile('^.+@+.+\.+.+$')
    if not pattern.match(email):
        raise ValidationError('Invalid Email Format')

def validate_password(password):
    if len(password) < MINIMUM_PASSWORD_LENGTH:
        raise ValidationError('Password is too short')

class SignupView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data.get('email', None)
            name     = data.get('name', None)
            phone    = data.get('phone', None)
            password = data.get('password', None)

            # KEY_ERROR check
            if not(password and email and name and phone):
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

            # validation check
            validate_email(email)
            validate_password(password)
            
            # unique check
            user = User.objects.filter(Q(email=email) | Q(name=name) | Q(phone=phone)) 
            if not user:
                User.objects.create(
                    email    = email,
                    name     = name,
                    phone    = phone,
                    password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                )
                return JsonResponse({'message': 'SUCCESS'}, status=200)
            return JsonResponse({'message': 'USER_ALREADY_EXISTS'}, status=409)


        except ValidationError as e:    
            trace_back = traceback.format_exc()
            print(f'{e}: {trace_back}')
            return JsonResponse({'message': 'VALIDATION_ERROR'}, status=422)
        
    def get(self, request):
        users = list(User.objects.values())

        return JsonResponse({'data': users}, status=200)

class LoginView(View):
    def post(self, request):
        data     = json.loads(request.body)
        email    = data.get('email', None)
        name     = data.get('name', None)
        phone    = data.get('phone', None)
        password = data.get('password', None)
        
        # key error check
        if not (password and (email or name or phone)):
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)        
            
        # valid user check  
        if User.objects.filter(Q(email=email) | Q(name=name) | Q(phone=phone)).exists():
            user = User.objects.get(Q(email=email) | Q(name=name) | Q(phone=phone))

            # password check
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                # JSON Web Token
                token = jwt.encode({'user_id': user.id}, SECRET['secret'], algorithm='HS256')
                return JsonResponse({'message': 'SUCCESS', 'access_token': token}, status=200) 
            
        return JsonResponse({'message': 'INVALID_ERROR'}, status=401)


