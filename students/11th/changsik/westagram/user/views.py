import json
import bcrypt
import jwt

from django.views import View
from django.http  import JsonResponse

from .models import User

SECRET_KEY = 'abc'

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({"message" : "email already exists"}, status = 400)
            if not '@' in data['email'] or not '.' in data['email']:
                return JsonResponse({"message" : "email form is mismatched"}, status = 401)
            if len(data['password']) < 8:
                return JsonResponse({"message" : "password form is mismatched"}, status = 402)
            hash_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            hash_pw = hash_pw.decode('utf-8')
            User(
                email    = data['email'],
                password = hash_pw,
            ).save()
            return JsonResponse({"message" : "SUCCESS"}, status = 200)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
        
class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try :
            if User.objects.filter(email = data['email']).exists():
                signin_user = User.objects.get(email = data['email'])
                post_password = data['password'].encode('utf-8')
                if bcrypt.checkpw(post_password, signin_user.password.encode('utf-8')) :
                    token = jwt.encode({'email':signin_user.email}, SECRET_KEY, algorithm = "HS256")
                    return JsonResponse({'token':token.decode()}, status = 200)
                return JsonResponse({"message" : "INVALID_USER"}, status = 402)
            return JsonResponse({"message" : "INVALID_USER"}, status = 401)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)