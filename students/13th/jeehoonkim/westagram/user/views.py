import json
import re

from django.views     import View
from django.db.models import Q
from django.http      import JsonResponse

from .models          import User

class SignUpView(View):
    def post(self, request):
        data     = json.loads(request.body)
        email    = data['email']
        name     = data['name']
        password = data['password']
        phone    = data['phone']

        email_pattern = '^\w+([-_.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'
        
        if password == '' or email == '':
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        if len(password)<8: 
            return JsonResponse({'message': 'PASSWORD IS NOT VALID'}, status=400)

        if re.match(email_pattern, email) == None:
            return JsonResponse({'message': 'EMAIL IS NOT VALID'}, status=400)

        if User.objects.filter(Q(email=email) | Q(name=name) | Q(phone=phone)).exists(): 
            return JsonResponse({'message': 'USER ALREADY EXISTS'}, status=400)
        
        User.objects.create(
            email    = email,
            name     = name,
            password = password,
            phone    = phone
        )

        return JsonResponse({'message': 'SUCCESS'}, status=201)

class SignInView(View):
    def post(self, request):
        data     = json.loads(request.body)
        email    = data['email']
        password = data['password']
        phone    = data['phone']
        
        if (phone or email) and password:
           try:
                User.objects.get(Q(phone=phone) | Q(email=email), password=password)
           except User.DoesNotExist:
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
           else:
                return JsonResponse({'message': 'SUCCESS'}, status=200)
        else:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

