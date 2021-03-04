import json
import re

from django.http  import JsonResponse
from django.views import View

from user.models import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            user_email    = data['email']
            user_password = data['password']

            # check password length
            if len(user_password) < 8:
                return JsonResponse({'message': 'Password is too short'}, status= 400)
            
            # check email
            p = re.compile("^[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-z]+$")
            if not p.match(user_email):
                return JsonResponse({'message': 'Check your email'}, status= 400)
            
            # check user
            exist_users = User.objects.all()
            for exist_user in exist_users:
                if user_email in exist_user.email:
                    return JsonResponse({'message': 'User already exists'}, status= 400)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status= 400)
        
        else:
            #User.objects.create(email=user_email, password=user_password)
            return JsonResponse({'message': 'SUCCESS'}, status= 200)
