import re
import json
from django.http      import JsonResponse 
from django.views     import View  
from .models          import User
from django.db.models import Q

class SignupView(View):

    def post(self, request) :
        data         = json.loads(request.body)
        email_check  = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-_]+\.[a-zA-Z0-9-.]{2,3}$')
        phone_check  = re.compile('^\d{3}-?\d{3,4}-?\d{4}$')

        if not (data['user_id'] and data['password']) :
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        elif not re.match('.{8}',data['password']) :
            return JsonResponse({'MESSAGE':'Password too short'}, status=400)
        elif email_check.match(data['user_id']) :
            if User.objects.filter(Q(user_name = data['user_name']) | Q(email = data['user_id'])).exists() :
                return JsonResponse({'MESSAGE':'Duplicate information'}, status=400)
            else :
                User.objects.create(
                    email     = data['user_id'],
                    user_name = data['user_name'],
                    name      = data['name'],
                    password  = data['password']
                )
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=201) 
        elif phone_check.match(data['user_id']):
            phone_number = ''.join(data['user_id'].split('-'))
            if User.objects.filter(Q(user_name = data['user_name']) | Q(phone_number = phone_number)).exists() :
                return JsonResponse({'MESSAGE':'Duplicate information'}, status=400)
            else :
                User.objects.create(
                    phone_number = phone_number,
                    user_name    = data['user_name'],
                    name         = data['name'],
                    password     = data['password']
                )           
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=201) 
        else :
            return JsonResponse({'MESSAGE':'Invalid email address or phone number'}, status=400)


class LoginView(View):
    
    def post(self, request) :
        data = json.loads(request.body)
        phone_number = ''.join(data['user_id'].split('-'))
        try :
            if not (data['user_id'] and data['password']) :
                return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
            elif (User.objects.get(user_name = data['user_id'], password = data['password']) or
                    User.objects.get(email = data['user_id'], password = data['password']) or
                    User.objects.get(phone_number = phone_number, password = data['password'])):
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
        except :
            return JsonResponse({"message": "INVALID_USER"}, status=401)