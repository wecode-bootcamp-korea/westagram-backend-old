import json
import bcrypt
import jwt

from django.http        import JsonResponse
from django.views       import View

from user.models    import User
from my_settings    import JWT_AUTH
from utils          import validate_length, validate_email, validate_password, validate_account, validate_mobile

class SignupView(View):
    def post(self, request):
        try:
            data  = json.loads(request.body)
            
            email    = data['email']
            password = data['password']
            account  = data.get('account')
            mobile   = data.get('mobile')

            if not validate_length(data):
                return JsonResponse({'MESSAGE' : 'DATA_TOO_LONG'}, status=400)
                
            if not validate_email(email):
                return JsonResponse({'MESSAGE' : 'INVALID_EMAIL'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE' : 'EMAIL_ALREADY_EXISTS'}, status=409)

            if not validate_password(password):
                return JsonResponse({'MESSAGE' : 'INVALID_PASSWORD'}, status=400)

            if account and User.objects.filter(account=account).exists():
                return JsonResponse({'MESSAGE' : 'ACCOUNT_ALREADY_EXISTS'}, status=409)

            if mobile and not validate_mobile(mobile):
                return JsonResponse({'MESSAGE' : 'INVALID_MOBILE'}, status=400)

            if mobile and User.objects.filter(mobile=mobile).exists():
                return JsonResponse({'MESSAGE' : 'MOBILE_ALREADY_EXISTS'}, status=409)

            User.objects.create(
                email    = email,
                password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                account  = account,
                mobile   = mobile
            )

        except json.decoder.JSONDecodeError:
            return JsonResponse({'MESSAGE' : 'REQUEST_WITHOUT_DATA'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)

class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data.get('email')
            password = data['password'].encode('utf-8')
            account  = data.get('account')
            mobile   = data.get('mobile')
           
            current_user = ''
            if email:
                current_user = User.objects.filter(email=email)
            if account:
                current_user = User.objects.filter(account=account)
            if mobile:
                current_user = User.objects.filter(mobile=mobile)

            if current_user and bcrypt.checkpw(password, current_user[0].password.encode('utf-8')):
                access_token = jwt.encode({'id':current_user[0].id}, JWT_AUTH['SECRET_KEY'], algorithm=JWT_AUTH['ALGORITHM'])
                return JsonResponse({'MESSAGE' : 'SUCCESS',
                    'access_token' : access_token}, status=200)

            return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status=401)
            
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
