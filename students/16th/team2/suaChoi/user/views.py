import json
import re

from django.http  import JsonResponse
from django.views import View

from .models import User

class SignupView(View):

    def post(self, request):

         try:
             data     = json.loads(request.body)
             name     = data['name']
             email    = data['email']
             password = data['password']

             email_rule = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

             # KEY ERROR
             if not email and password:
                 return JsonResponse({"message": "KEY_ERROR"}, status=400)

             # too short password
             if len(password) <  8:
                 return JsonResponse({"message":"NOT_VALID_PASSWORD"}, status=400)

             # bend email rule
             if not email_rule.match(email):
                 return JsonResponse({"message": "NOT_VALID_EMAIL"}, status=400)

             # exist email
             if User.objects.filter(email=email).exists():
                 return JsonResponse({"message": "EXIST_EMAIL"}, status=400)

             if not User.objects.filter(email=email).exists():
                 User.objects.create(
                     name     = name,
                     email    = email,
                     password = password
                 )
                 return JsonResponse({"message": "SUCCESS"}, status=200)

         except:
             return JsonResponse({"message": "KEY_ERROR"}, status=400)


class LoginView(View):

    def post(self, request):

        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if User.objects.filter(email=email).exists():
                # EXIST EMAIL & VALID PASSWORD
                if User.objects.get(email=email).password == password:
                    return JsonResponse({"message": "SUCCESS"}, status=200)
                # EXIST EMAIL & INVALED PASSWORD:
                return JsonResponse({"message": "INVALID_PASSWORD"}, status=401)
            # INVALED_EMAIL
            return JsonResponse({"message": "INVALID_EMAIL"}, status=401)

        except:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


