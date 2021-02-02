import json, re


from django.http   import JsonResponse, HttpResponse
from django.views  import View

from user.models   import (
    User
)

email_regex              = re.compile(r'.*[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+.*')
password_regex           = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
phone_regex              = re.compile(r'[0-9]{3}-[0-9]{4}-[0-9]{4}')

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            name                     = data['name']
            phone                    = data['phone']
            email                    = data['email']
            password                 = data['password']
            username                 = data['username']

            if name == "":
                return JsonResponse({"MESSAGE" : "NAME_REQUIRED"}, status=400)

            if phone == "" and email == "":
                return JsonResponse({"MESSAGE" : "EMAIL_OR_PHONE_NUMBER_REQUIRED"}, status=400)

            if username == "":
                return JsonResponse({"MESSAGE" : "USERNAME_REQUIRED"}, status=400)

            if password == "":
                return JsonResponse({"MESSAGE" : "PASSWORD_REQUIRED"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"MESSAGE": "EMAIL_EXISTS"}, status=400)
                
            if User.objects.filter(username=username).exists():
                return JsonResponse({"MESSAGE" : "USERNAME_EXISTS"}, status=400)

            if (email_regex.search(str(email)) != None) == False:
                return JsonResponse({"MESSAGE" : "EMAIL_VALIDATION"}, status=400)

            if (password_regex.match(str(password)) != None) == False:
                return JsonResponse({"MESSAGE" : "PASSWORD_VALIDATION"}, status=400)

            if (phone_regex.match(str(phone)) != None) == False:
                return JsonResponse({"MESSAGE" : "PHONE_VALIDATION"}, status=400)

            User.objects.create(
                name     = name, 
                email    = email, 
                phone    = phone,
                password = password, 
                username = username
            )

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)
        
        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status=400)
