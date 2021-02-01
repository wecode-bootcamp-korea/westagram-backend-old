import json, re, traceback, bcrypt

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Q
from django.core.exceptions import ValidationError

from .models                import User

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
            if password and email and name and phone:

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

            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except ValidationError as e:    
            trace_back = traceback.format_exc()
            print(f'{e}: {trace_back}')
            return JsonResponse({'message': 'VALIDATION_ERROR'}, status=422)
        
    def get(self, request):
        users = list(User.objects.values())

        return JsonResponse({'data': users}, status=200)

