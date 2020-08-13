import json, traceback, bcrypt, jwt

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from westagram.settings     import SECRET_KEY 

from .models import User

class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)

        if not data['email'] or not data['password']:
            return JsonResponse({'message' : 'No value entered'}, status = 400)

        try: 
            signup_user = User(
                email    = data['email'],
                password = data['password'],
            )
            signup_user.full_clean()
            signup_user.password = signup_user.password.encode('utf-8')
            signup_user.password = bcrypt.hashpw(signup_user.password, bcrypt.gensalt())
            signup_user.password = signup_user.password.decode('utf-8')
            signup_user.save()
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        except ValidationError as e:
            trace_back = traceback.format_exc()
            print(f"{e} : {trace_back}")
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        
        return JsonResponse({'message' : 'Invalid format or Duplicated Email'}, status = 400)

    # 유저 리스트
    def get(self, request):
        user = User.objects.values()
        return JsonResponse({'user' : list(user)}, status = 200)

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        if not data['email'] or not data['password']:
            return JsonResponse({'message' : 'No value entered'}, status = 400)
            
        try:
            if User.objects.filter(email = data['email']).exists():
                signin_user = User.objects.get(email = data['email'])
                input_password = data['password']
                if bcrypt.checkpw(input_password.encode('utf-8'), signin_user.password.encode('utf-8')):
                    token = jwt.encode({'user_id' : signin_user.id}, SECRET_KEY, algorithm = 'HS256')
                    # token = jwt.decode(token, SECRET_KEY, algorithm = 'HS256')
                    token = token.decode('utf-8')
                    return JsonResponse({'token' : token}, status = 200)

            return JsonResponse({'message' : 'INVALID_USER'}, status = 401)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

    def get(self, request):
        user = User.objects.values()
        return JsonResponse({'user' : list(user)}, status = 200)
