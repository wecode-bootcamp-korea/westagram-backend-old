import json, re, bcrypt, jwt

from django.http     import JsonResponse
from django.views    import View

from .models         import Account

MINIMUN_PASSWORD_LENGTH = 8

class UserSignUpView(View):
    def post(self, request):
        try:
            data       = json.loads(request.body)
            username   = data.get('username', None)
            email      = data.get('email', None)
            password   = data.get('password', None)
            phone_num  = data.get('phone_num', None)

            if email and password:
                email_form = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
                
                if not email_form.match(str(email)):
                    return JsonResponse({'MESSSAGE': 'INVALID_EMAIL'}, status=400)

                if len(password) < MINIMUN_PASSWORD_LENGTH:
                    return JsonResponse({'MESSSAGE': 'PASSWORD_IS_SHORT'}, status=400)

                if Account.objects.filter(email=data['email']).exists():
                    return JsonResponse({'MESSSAGE': 'ALREADY_USE_EMAIL'}, status=400)

                user_data = Account.objects.create(
                        username   = username,
                        email      = email,
                        password   = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                        phone_num  = phone_num
                        )
                return JsonResponse({'MESSSAGE': 'SUCCESS'}, status=200)

            return JsonResponse({'MESSSAGE': 'KEY_ERROR'}, status=400)

        except KeyError:
            return JsonResponse({'MESSSAGE': 'KEY_ERROR'}, status=400)

class UserSignInView(View):
    def post(self, request):
        try:
            data      = json.loads(request.body)
            email     = data['email']
            password  = data['password']

            if Account.objects.filter(email=email).exists():
                login_user = Account.objects.get(email=email)

                if bcrypt.checkpw(password.encode('utf-8'), login_user.password.encode('utf-8')):
                    access_token=jwt.encode({'id' : login_user.id}, 'secret', algorithm='HS256')
                    return JsonResponse({'MESSSAGE': 'SUCCESS', 'ACCESS_TOKEN': access_token}, status=200)
                
                return JsonResponse({'MESSSAGE': 'INVALID_PASSWORD'}, status=401)
            
            return JsonResponse({'MESSSAGE': 'INVALID_USER'}, status=401)
        
        except KeyError:
            return JsonResponse({'MESSSAGE': 'KEY_ERROR'}, status=400)
