import json

from django.http     import JsonResponse, HttpResponse
from django.views    import View

from user.models import User


class SignUpView(View):

MINIMUM_PASSWORD_LENGTH = 8

    def post(self, request):
        
        try:
            data     = json.loads(request.body)
            name     = data['name']
            email    = data['email']
            password = data['password']
            phone    = data['phone']
        
            if name and email and password and phone:
                    
                if User.objects.filter(name=name).exists():
                    return JsonResponse({'message': 'ID_ALREADY_EXISTS'}, status=400)
                    return HttpResponse(status=400)
                    
                if User.objects.filter(email=email).exists():
                    return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'}, status=400)

                if User.objects.filter(phone=phone).exists():
                    return JsonResponse({'message': 'PHONE_NUMBER_ALREADY_EXISTS'}, status=400)
                
                if '@' not in email or '.' not in email:
                    return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)

                if len(password) < MINIMUM_PASSWORD_LENGTH:
                    return JsonResponse({'message': 'PASSWORD_VALIDATION_ERROR'}, status=400)

                User.objects.create(name=name, email=email, password=password, phone=phone)

                return JsonResponse({'message': 'SUCCESS'}, status=200)
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

