import json

from django.http   import JsonResponse, HttpResponse;
from django.views  import View

from user.models   import (
    User
)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        name          = data['name']
        email         = data['email']
        password      = data['password']
        username      = data['username']

        if User.objects.filter(email=email).exists():
                return JsonResponse({"MESSAGE": "EMAIL_KEY_ERROR"}, status=400)
             
        if '@' and '.' not in email:
                return JsonResponse({"MESSAGE" : "NOT_EMAIL_SYNTAX"}, status=400)
            
        if len(password) <= 8:
            return JsonResponse({"MESSAGE" : "PASSWORD_KEY_ERROR"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"MESSAGE" : "USERNAME_EXISTS"}, status=400)

        User.objects.create(
            name     = name, 
            email    = email, 
            password = password, 
            username = username)


        return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)
