import json

from django.views import View
from django.http import JsonResponse

from user.models import User

class UserView(View):
    def post(self, request):
        data     = json.loads(request.body)
        name     = data.get('name')
        password = data.get('password')
        email    = data.get('email')
        phone    = data.get('phone')

        if email == None and phone == None and name == None:
            return JsonResponse({'MESSAGE': 'KEY_ERRORS'}, status=400)

        if email != None:
            if '@' not in email or '.' not in email:
                return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=400)

        if password == None:
            return JsonResponse({'MESSAGE': 'KEY_ERRORS'}, status=400)
        
        if len(password) < 8:
            return JsonResponse({'MESSAGE': 'INVALID_PASSWORD'}, status=400)
        
        if User.objects.filter(name=name).exists() or User.objects.filter(phone=phone).exists() or User.objects.filter(email=email).exists():
            return JsonResponse({'MESSAGE': 'EXIST_USER'}, status=400)

        User.objects.create(name=name, password=password, email=email, phone=phone)
        
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        