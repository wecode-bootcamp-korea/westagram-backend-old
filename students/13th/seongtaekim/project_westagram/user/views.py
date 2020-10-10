import re
import json
from django.http      import JsonResponse 
from django.views     import View
from .models          import User
from django.db.models import Q

class Loginview(View):

    def post(self, request) :
        data         = json.loads(request.body)
        phone_number = ''.join(data['phone_number'].split('-'))
        email_check  = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-_]+\.[a-zA-Z0-9-.]{2,3}$')
        if not (data['email'] and data['password']) :
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400) 
        elif not email_check.match(data['email']) :
            return JsonResponse({'MESSAGE':'Invalid email address'}, status=400)
        elif not re.match('.{8}',data['password']) :
            return JsonResponse({'MESSAGE':'Password too short'}, status=400)
        elif User.objects.filter(Q(user_name = data['user_name']) | Q(phone_number = phone_number) | Q(email = data['email'])).exists() :
            return JsonResponse({'MESSAGE':'Duplicate information'}, status=400)
        else : 
            User.objects.create(
                password     = data['password'],
                user_name    = data['user_name'],
                email        = data['email'],
                phone_number = phone_number
            )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)    
