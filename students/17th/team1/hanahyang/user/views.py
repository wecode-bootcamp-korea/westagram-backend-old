import json, re, traceback

from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Q
from django.core.exceptions import ValidationError

from .models                import User

def validate_email(email):
    p = re.compile('^.+@+.+\.+.+$')
    if not p.match(email):
        raise ValidationError('Invalid Email Format')

def validate_password(password):
    if len(password) < 8:
        raise ValidationError('Password is too short')

class SignupView(View):
    def post(self, request):
        try:
            data     = json.load(request)
            email    = data.get('email', None)
            name     = data.get('name', None)
            phone    = data.get('phone', None)
            password = data.get('password', None)

            if email: 
                validate_email(email)

            if password:
                validate_password(password)
                if email or name or phone:
                    has_email = User.objects.filter(Q(email=email) & Q(email__isnull=False))
                    has_name  = User.objects.filter(Q(name=name) & Q(name__isnull=False))
                    has_phone = User.objects.filter(Q(phone=phone) & Q(phone__isnull=False))
                    
                    if not (has_email or has_name or has_phone):
                        User.objects.create(
                            email    = email,
                            name     = name,
                            phone    = phone,
                            password = password
                        )
                        return JsonResponse({'message': 'SUCCESS'}, status=200)
                    return JsonResponse({'message': 'ALREADY_EXISTS'}, status=409)

            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except ValidationError as e:    
            trace_back = traceback.format_exc()
            print(f'{e}: {trace_back}')
            return JsonResponse({'message': 'ValidationError'}, status=422)
        
