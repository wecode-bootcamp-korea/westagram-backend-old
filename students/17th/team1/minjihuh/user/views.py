import json

from django.http   import JsonResponse, HttpResponse;
from django.views  import View

from user.models   import (
    User
)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            name          = data['name']
            email         = data['email']
            password      = data['password']
            username      = data['username']
            MINIMUM_PASSWORD_LEN = 8

            if User.objects.filter(email=email).exists():
                    return JsonResponse({"MESSAGE": "EMAIL_EXISTS"}, status=400)
                
            if '@' and '.' not in email:
                    return JsonResponse({"MESSAGE" : "INVALID_EMAIL_SYNTAX"}, status=400)
                
            if len(password) <= MINIMUM_PASSWORD_LEN:
                return JsonResponse({"MESSAGE" : "PASSWORD_MUST_BE_LONGER_THAN_EIGHT_LETTERS"}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"MESSAGE" : "USERNAME_EXISTS"}, status=400)

            User.objects.create(
                name     = name, 
                email    = email, 
                password = password, 
                username = username
            )

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)
        except KeyError:
            return JsonResponse({"MESSAGE" : "USERNAME_EXISTS"}, status=400)
