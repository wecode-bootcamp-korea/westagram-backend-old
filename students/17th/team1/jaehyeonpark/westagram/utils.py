import json, bcrypt

from django.http      import JsonResponse
from django.db.models import Q

from user.models      import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            data         = json.loads(request.body)
            email        = data.get('email')
            phone_number = data.get('phone_number')
            account      = data.get('account')
            password     = data['password']

            if not (email or account or phone_number):
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

            if not User.objects.filter(Q(email=email)|Q(phone_number=phone_number)|Q(account=account)).exists():
                return JsonResponse({'message':'INVALID_USER'}, status=401)

            user = User.objects.get(Q(email=email)|Q(phone_number=phone_number)|Q(account=account))

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
            
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        return func(self, request, data, user)

    return wrapper