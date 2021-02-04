import json, re
import bcrypt
import jwt

from json.decoder       import JSONDecodeError

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from .models            import User
from my_settings        import SECRET_KEY

class UserView(View):
    def post(self, request):
        email_valid     = "[0-9a-zA-Z_-]+[@]{1}[0-9a-zA-Z_-]+[.]{1}[a-zA-Z]+"
        password_valid  = ".{8,}"
        name_valid      = "^(?=.*[a-z])[0-9a-zA-Z]+"
        try:
            data            = json.loads(request.body)
            email           = data['email']
            password        = data['password']
            hash_password   = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            name            = data['name']
            phone_number    = data['phone_number']
            
            if User.objects.filter(Q(email=email)|Q(name=name)|Q(phone_number=phone_number)).exists():
                return JsonResponse({'message' : 'EXISTING_USER'}, status=400)
            if not re.search(email_valid, email):
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status=400)
            if ' 'in (email and password):
                return JsonResponse({'message' : 'MEANINLESS_SPACE'}, status=400)
            if not re.search(password_valid, password):
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status=400)
            if not re.search(name_valid, name):
                return JsonResponse({'message' : 'INVALID_NAME'}, status=400)
            User.objects.create(
                    email=email,
                    password=hash_password.decode('utf-8'),
                    name=name,
                    phone_number=phone_number
                    )
            return JsonResponse({'meassage' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message' : 'NOTHING_INPUT'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            password        = data.get('password', None)
            login_id        = data.get('login_id', None)
            
            if not (login_id and password):
                return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
            
            if not User.objects.filter(Q(email=login_id) | Q(name=login_id) | Q(phone_number=login_id)).exists():
                return JsonResponse({'message' : 'INVALID_USER'}, status=401)
            user = User.objects.get(Q(email=login_id)|Q(name=login_id)|Q(phone_number=login_id))
            
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message' : 'INVALID_USER'}, status=401)
            access_token = jwt.encode({'user' : user.id}, SECRET_KEY, algorithm='HS256')
            return (JsonResponse({'message' : 'SUCCESS', "token" : access_token}, status=200))

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message' : 'NOTHING_INPUT'}, status=400)
