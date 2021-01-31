import json, re

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.db.models import Q

from user.models import User

class SingUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        email         = data.get('email', None)
        mobile_number = data.get('mobile_number', None)
        full_name     = data.get('full_name', None)
        username      = data.get('username', None)
        password      = data.get('password', None)

        email_pattern           = re.compile('[^@]+@[^@]+\.[^@]+')
        PASSWORD_MINIMUM_LENGTH = 8

        if not (
            (email or mobile_number) 
            and password 
            and full_name 
            and username 
            and password
        ):
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        if email:
            if not re.match(email_pattern, email):
                return JsonResponse({'message':'EMAIL_VALIDATION_ERROR'}, status=400)

        if len(data['password']) < PASSWORD_MINIMUM_LENGTH:
            return JsonResponse({'message':'PASSWORD_VALIDATION_ERROR'}, status=400)

        if User.objects.filter(
            Q(email         = data.get('email', None)) |
            Q(mobile_number = data.get('mobile_number', None)) |
            Q(username      = data['username'])
        ).exists():
            return JsonResponse({'message':'ALREADY_EXISTS'}, status=409)

        User.objects.create(
            email         = data.get('email', None),
            mobile_number = data.get('mobile_number', None),
            full_name     = data['full_name'],
            username      = data['username'],
            password      = data['password']
        )
        return JsonResponse({'message':'SUCCESS'}, status=201)
