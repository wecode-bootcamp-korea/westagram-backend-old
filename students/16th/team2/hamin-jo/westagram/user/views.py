import json
import re
import bcrypt
import jwt

from django.views import View
from django.http import JsonResponse

from user.models import User

class UserView(View):
    def post(self, request):
        try:
            data           = json.loads(request.body)
            name           = data.get('name')
            phone          = data.get('phone')
            password       = data.get('password')
            email          = data.get('email')
            email_regex    = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            password_regex = '[A-Za-z0-9@#$]{8,12}'
            encoded_pw     = password.encode('utf-8')
            hashed_pw      = bcrypt.hashpw(encoded_pw, bcrypt.gensalt())
            decoded_pw     = hashed_pw.decode('utf-8')

            if 'email' in data.keys():
                if not (re.search(email_regex,email)):
                    return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=400)

                if User.objects.filter(email=email).exists():
                    return JsonResponse({'MESSAGE': 'EXIST_USER'}, status=400)
            else:
                return JsonResponse({'MESSAGE': 'KEY_ERRORS; email'}, status=400)

            if 'password' in data.keys():
                if not (re.search(password_regex, password)):
                    return JsonResponse({'MESSAGE': 'INVALID_PASSWORD'}, status=400)
            else:
                return JsonResponse({'MESSAGE': 'KEY_ERRORS; password'}, status=400)

            if phone:
                if User.objects.filter(phone=phone).exists():
                    return JsonResponse({'MESSAGE': 'EXIST_USER'}, status=400)

            User.objects.create(name= name, password= decoded_pw, email= email, phone= phone)

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERRORS'}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data        = json.loads(request.body)
            email       = data.get('email')
            password    = data.get('password').encode('utf-8')
            
            if email:
                if User.objects.filter(email= email).exists():
                    user       = User.objects.get(email= email)
                    user_id    = user.id
                    user_pw    = user.password
                    
                    if bcrypt.checkpw(password, user_pw.encode('utf-8')):
                        print(234)
                        token  = jwt.encode( {'user-id':user_id}, 'secret', algorithm='HS256')
                        
                        return JsonResponse({"token":token}, status= 200)

                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
            return JsonResponse({'MESSAGE': 'KEY_ERRORS'}, status=400)

        except:
             return JsonResponse({'MESSAGE': 'KEY_ERRORSSSS'}, status=400)
        