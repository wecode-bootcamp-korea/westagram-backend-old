import re
import json
import jwt
import bcrypt
from django.http      import JsonResponse 
from django.views     import View  
from user.models      import User
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

        hashed_password  = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        decoded_password = hashed_password.decode('utf-8')
        try :
            new_user     = User(name = data['name'], password  = decoded_password)
        except :
            new_user     = User(password  = decoded_password)
            
        if email_check.match(data['user_id']) :
            if User.objects.filter(Q(user_name = data['user_name']) | Q(email = data['user_id'])).exists() :
                return JsonResponse({'MESSAGE':'Duplicate information'}, status=400)
            else :
                new_user.user_name = data['user_name']                
                new_user.email     = data['user_id']
                new_user.save()
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=201) 
        elif phone_check.match(data['user_id']):
            phone_number = ''.join(data['user_id'].split('-'))
            if User.objects.filter(Q(user_name = data['user_name']) | Q(phone_number = phone_number)).exists() :
                return JsonResponse({'MESSAGE':'Duplicate information'}, status=400)
            else :
                new_user.user_name    = data['user_name']
                new_user.phone_number = phone_number
                new_user.save()
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=201) 
        else :
            return JsonResponse({'MESSAGE':'Invalid email address or phone number'}, status=400)

class LoginView(View):
    def __init__(self):
        self.SECRET = 'secret'

    def post(self, request) :
        data             = json.loads(request.body)
        phone_number     = ''.join(data['user_id'].split('-'))
        try :
            if not (data['user_id'] and data['password']) :
                return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

            user1 = User.objects.get(Q(user_name = data['user_id']) | Q(email = data['user_id']) | Q(phone_number = data['user_id']))
            if bcrypt.checkpw(data['password'].encode('utf-8'), user1.password.encode('utf-8')):
                access_token = jwt.encode({'id' : user1.id}, self.SECRET, algorithm = 'HS256')
                return JsonResponse({'MESSAGE':'SUCCESS','token':access_token.decode('utf-8')}, status=201)
            else : 
                return JsonResponse({"MESSAGE": "WRONG PASSWORD"}, status=401)
        except :
            return JsonResponse({"MESSAGE": "INVALID_USER"}, status=401)
