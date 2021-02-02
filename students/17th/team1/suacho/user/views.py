import json, re
from json.decoder import JSONDecodeError

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.db.models import Q

from user.models import User


PASSWORD_MINIMUM_LENGTH = 8

class SingUpView(View):
    def post(self, request):
        try:   
            data = json.loads(request.body)

            email         = data.get('email', None)
            mobile_number = data.get('mobile_number', None)
            full_name     = data.get('full_name', None)
            username      = data.get('username', None)
            password      = data.get('password', None)

            email_pattern         = re.compile('[^@]+@[^@]+\.[^@]+')
            mobile_number_pattern = re.compile('^[0-9]{1,15}$')
            username_pattern      = re.compile('^(?=.*[a-z])[a-z0-9_.]+$')

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
            
            if mobile_number:
                if not re.match(mobile_number_pattern, mobile_number):
                    return JsonResponse({'message':'MOBILE_NUMBER_VALIDATION_ERROR'}, status=400)

            if not re.match(username_pattern, username):
                return JsonResponse({'message':'USERNAME_VALIDATION_ERROR'}, status=400)

            if len(data['password']) < PASSWORD_MINIMUM_LENGTH:
                return JsonResponse({'message':'PASSWORD_VALIDATION_ERROR'}, status=400)

            if User.objects.filter(
                Q(email         = data.get('email', 1)) |
                Q(mobile_number = data.get('mobile_number', 1)) |
                Q(username      = data['username'])
            ).exists():
                return JsonResponse({'message':'ALREADY_EXISTS'}, status=409)
            
            User.objects.create(
                email         = email,
                mobile_number = mobile_number,
                full_name     = full_name,
                username      = username,
                password      = password
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)
        
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
