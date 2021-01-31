import json
import re

from django.http    import JsonResponse
from django.views   import View

from user.models    import User

class UserView(View):
    def get(self, request):
        users       = User.objects.all()
        user_list   = []
        for user in users:
            user_info = {
                "email"         : user.email,
                "password"      : user.password,
                "name"          : user.name,
                "phone_number"  : user.phone_number
                }
            user_list.append(user_info)
        
        return JsonResponse({user_list}, status=200)

    def post(self, request):
        data            = json.loads(request.body)
        email_valid     = "([0-9a-zA-Z_-]+)[@]{1}([0-9a-zA-Z_-]+)[.]{1}[a-zA-Z]{3}"
        password_valid  = ".{8,}"
        name_valid      = "[a-zA-z]"

        try:
            email           = data['email']
            password        = data['password']
            name            = data['name']
            phone_number    = data['phone_number']

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message' : 'EXISTING_USER'}, status=409)
            elif not re.search(email_valid, email):
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status=409)
            elif ' 'in (email and password):
                return JsonResponse({'message' : 'MEANINLESS_SPACE'}, status=409)
            elif not re.search(password_valid, password):
                return JsonResponse({'message' : 'SHORT_PASSWORD'}, status=409)
            elif not re.search(name_valid, name):
                return JsonResponse({'message' : 'INVALID_NAME'}, status=409)
            User.objects.create(
                    email=email,
                    password=password,
                    name=name,
                    phone_number=phone_number
                    )
            return JsonResponse({'meassage' : 'SUCCESS'}, status=200)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message' : 'INPUT_NOTING'}, status=400)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

