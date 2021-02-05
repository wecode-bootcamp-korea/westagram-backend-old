import re
import jwt
import json
import bcrypt

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Q

from .models                import User, Follow
from .utils                 import login_decorator
from my_settings            import SECRET

MINIMUM_PASSWORD_LENGTH = 8

def validate_email(email):
    pattern = re.compile('^.+@+.+\.+.+$')
    if not pattern.match(email):
        return False
    return True

def validate_password(password):
    if len(password) < MINIMUM_PASSWORD_LENGTH:
        return False
    return True

def validate_phone(phone):
    pattern = re.compile('^[0]\d{2}\d{3,4}\d{4}$')
    if not pattern.match(phone):
        return False
    return True

class SignupView(View):
    def post(self, request):
        data     = json.loads(request.body)
        email    = data.get('email', None)
        name     = data.get('name', None)
        phone    = data.get('phone', None)
        password = data.get('password', None)

        # KEY_ERROR check
        if not(password and email and name and phone):
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        # validation check
        if not validate_email(email):
            return JsonResponse({'message': 'EMAIL_VALIDATION_ERROR'}, status=422)

        if not validate_password(password):
            return JsonResponse({'message': 'PASSWORD_VALIDATION_ERROR'}, status=422)

        if not validate_phone(phone):
            return JsonResponse({'message': 'PHONE_VALIDATION_ERROR'}, status=422)
        
        # unique check
        if User.objects.filter(Q(email=email) | Q(name=name) | Q(phone=phone)).exists():
            return JsonResponse({'message': 'USER_ALREADY_EXISTS'}, status=409)

        User.objects.create(
            email    = email,
            name     = name,
            phone    = phone,
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )
        return JsonResponse({'message': 'SUCCESS'}, status=200)

        
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
        
        # KEY_ERROR check
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
            
            return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)

        return JsonResponse({'message': 'INVALID_USER'}, status=401)

class FollowView(View):
    @login_decorator 
    def post(self, request):
        data           = json.loads(request.body)
        follow_user_id = data.get('follow_user', None)

        # KEY_ERROR check
        if not follow_user_id:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        from_user = request.user
        to_user   = User.objects.get(id=follow_user_id)
        follow    = Follow.objects.filter(from_user=from_user, to_user=to_user)
        
        if follow:
            follow[0].delete()
            message = 'Unfollowing'
        else:
            Follow.objects.create(
                from_user = from_user,
                to_user   = to_user, 
            )
            message = 'Following'

        return JsonResponse({'message': message}, status=200)

        
        

