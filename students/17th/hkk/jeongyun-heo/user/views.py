import json

from django.http     import JsonResponse, HttpResponse
from django.views    import View

from user.models import User

class SignUpView(View):

    def post(self, request):
        # print(request.body)
        data     = json.loads(request.body)
        # print(data)
        name     = data['name']
        email    = data['email']
        password = data['password']
        phone    = data['phone']
        
        try:
            if name and email and password and phone:
                    
                if User.objects.filter(name=name).exists():
                    return JsonResponse({'message': 'ID already exists'}, status=400)
                    
                if User.objects.filter(email=email).exists():
                    return JsonResponse({'message': 'Email already exists'}, status=400)

                if User.objects.filter(phone=phone).exists():
                    return JsonResponse({'message': 'Phone number already exists'}, status=400)
                
                if '@' not in email or '.' not in email:
                    return JsonResponse({'message': 'Invalid email'}, status=400)

                if len(password) < 8:
                    return JsonResponse({'message': 'Password must be at least 8 characters'}, status=400)

                User.objects.create(name=name, email=email, password=password, phone=phone)

                return JsonResponse({'message': 'SUCCESS'}, status=200)
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

