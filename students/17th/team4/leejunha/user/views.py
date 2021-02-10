import json

from django.views import View
from django.http  import JsonResponse

from .models      import Account

class UserSignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email        = data['email']
            password     = data['password']
            user_name    = data['user_name']
            phone_number = data['phone_number']         

            if len(password) < 8:
                return JsonResponse({'MESSAGE' : 'INVALID_PASSWORD'}, status = 400)

            if '@' not in email or '.' not in email:
                return JsonResponse({'MESSAGE' : 'INVALID_EMAIL'}, status = 400)
            
            if Account.objects.filter(phone_number = phone_number).exists():
                return JsonResponse({'MESSAGE' : 'INVALID_PHONE_NUMBER'}, status = 400)
                
            if Account.objects.filter(user_name = user_name).exists():
                return JsonResponse({'MESSAGE' : 'INVALID_USER_NAME'}, status = 400)
            
            if Account.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE' : 'INVALID_EMAIL'}, status = 400)
                
            else:
                Account.objects.create(
                    email        = email,
                    password     = password,
                    user_name    = user_name,
                    phone_number = phone_number
            )        
                return JsonResponse({'message' : 'SUCCESS'}, status = 201)
                
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status = 400)
