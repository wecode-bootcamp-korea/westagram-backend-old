import json, re
from django.http    import JsonResponse

from django.views   import View
from .models        import User


class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)

        email    = data['email']
        password = data['password']

        if not data['email']:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        elif not data['password']:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        
        if User.objects.filter(email=email):
            return JsonResponse({'message' : 'Already Exists'}, status = 400)

        regex_email    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
        regex_password = '\S{8,25}'
        if not re.match(regex_email, email):
            return JsonResponse({'message' : 'Invalid Email'}, status = 400)
        elif not re.match(regex_password, password):
            return JsonResponse({'message' : 'Invalid Password'}, status = 400) 

        User.objects.create(email=email, password=password)
        return JsonResponse({'message': 'Signup Success!'}, status=200)