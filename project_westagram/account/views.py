import json
import bcrypt
import jwt

from project_westagram.settings import SECRET_KEY
from django.views               import View
from django.http                import JsonResponse,HttpResponse
from .models                    import Account

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if Account.objects.filter(email =data['email']).exists():
                return HttpResponse(status=400)
            password = data['password'].encode('utf-8')
            password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())
            password_crypt = password_crypt.decode('utf-8')

            Account(
                email     =data['email'],
                password  =data['password'],
                ).save()
                
            return HttpResponse(status=200)
        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"},status =400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
             if Account.objects.filter(email = data['email']).exists() :
               user = Account.objects.get(email = data['email'])
             if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                 token = jwt.encode({'email' : data['email']}, SECRET_KEY, algorithm = "HS256")
                 token = token.decode('utf-8')

                 return JsonResponse({"token" : token }, status=200)

             else:
                 return HttpResponse(status=401)

             return HttpResponse(status=400)

        except KeyError:
             return JsonResponse({"message":"INVALID_KEYS"}, status = 400)

class TokenCheckView(View):
    def post(self,request):
        data = json.loads(request.body)

        user_token_info = jwt.decode(data['token'], SECRET_KEY, algorithm = 'HS256')

        if Account.objects.filter(email=user_token_info['email']).exists() :
            return HttpResponse(status=200)

        return HttpResponse(status=403)
