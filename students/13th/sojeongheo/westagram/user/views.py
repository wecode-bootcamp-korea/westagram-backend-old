import json

from django.views   import View
from django.http    import HttpResponse, JsonResponse
from user.models    import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
    
        user_name       = data['user_name']
        email           = data['email']
        phone_number    = data['phone_number']
        password        = data['password']
         

        if not data.get('user_name') or not data.get('email'):
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)        
        
        if len(password) < 8:
            return JsonResponse({"message":"password too short"}, status = 400)

        if '@' not in email or '.' not in email:
            return JsonResponse({"message":"invalid email address"}, status = 400)

        if User.objects.filter(user_name = user_name).exists():
            return JsonResponse({"message":"username already exists"}, status = 400)

        if User.objects.filter(email = email).exists():
            return JsonResponse({"message":"email already exists"}, status = 400)
        
        if User.objects.filter(phone_number = phone_number).exists():
            return JsonResponse({"message":"phone number already exists"}, status = 400)
        
        else:
            User.objects.create(
                user_name       = user_name,
                email           = email,
                phone_number    = phone_number,
                password         = password,
            )
        
        return JsonResponse({"message": "SUCCESS"}, status = 200)

