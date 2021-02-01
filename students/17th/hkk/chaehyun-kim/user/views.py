import json
import re

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q

from .models            import User

class UserView(View):
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
            if User.objects.filter(Q(email=email)|Q(name=name)|Q(phone_number=phone_number)).exists():
                return JsonResponse({'message' : 'EXISTING_USER'}, status=409)
            if not re.search(email_valid, email):
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status=409)
            if ' 'in (email and password):
                return JsonResponse({'message' : 'MEANINLESS_SPACE'}, status=409)
            if not re.search(password_valid, password):
                return JsonResponse({'message' : 'SHORT_PASSWORD'}, status=409)
            if not re.search(name_valid, name):
                return JsonResponse({'message' : 'INVALID_NAME'}, status=409)
            User.objects.create(
                    email=email,
                    password=password,
                    name=name,
                    phone_number=phone_number
                    )
            return JsonResponse({'meassage' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
