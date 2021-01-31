import json

from django.http    import JsonResponse
from django.views   import View

from user.models    import User

class SignupView(View):
    def post(self, request):
        try:
            data  = json.loads(request.body)
            
            email        = data['email']
            password     = data['password']
            account      = data.get('account')
            phone_number = data.get('phone_number')

            if len(email) > 100 or len(password) > 100:
                return JsonResponse({'MESSAGE' : 'DATA_TOO_LONG'}, status=400)
                
            if '@' not in email or '.' not in email:
                return JsonResponse({'MESSAGE' : 'INVALID_EMAIL'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE' : 'EMAIL_ALREADY_EXIST'}, status=409)

            if len(password) < 8:
                return JsonResponse({'MESSAGE' : 'INVALID_PASSWORD'}, status=400)

            if account:
                if len(account) > 20:
                    return JsonResponse({'MESSAGE' : 'DATA_TOO_LONG'}, status=400)
                if User.objects.filter(account=account).exists():
                    return JsonResponse({'MESSAGE' : 'ACCOUNT_ALREADY_EXIST'}, status=409)

            if phone_number:
                if len(phone_number) > 12:
                    return JsonResponse({'MESSAGE' : 'DATA_TOO_LONG'}, status=400)
                if User.objects.filter(phone_number=phone_number).exists():
                    return JsonResponse({'MESSAGE' : 'PHONE_NUMBER_ALREADY_EXIST'}, status=409)

            User.objects.create(
                email        = email,
                password     = password,
                account      = account,
                phone_number = phone_number
            )

        except json.decoder.JSONDecodeError:
            return JsonResponse({'MESSAGE' : 'REQUEST_WITHOUT_DATA'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)

class LoginView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data.get('email')
            password     = data['password']
            account      = data.get('account')
            phone_number = data.get('phone_number')
           
            login_user = ''
            if email:
                login_user = User.objects.filter(email=email)
            if account:
                login_user = User.objects.filter(account=account)
            if phone_number:
                login_user = User.objects.filter(phone_number=phone_number)

            if login_user:
                if not login_user.exists() or login_user[0].password != data['password']:
                    return JsonResponse({'MESSAGE' : 'INVALID_USER'}, status=401)
            else:
                return JsonResponse({'MESSAGE' : 'REQUEST_WITHOUT_USER_DATA'}, status=401)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)

        return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=200)
