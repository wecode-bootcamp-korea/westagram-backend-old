import jwt
import bcrypt
import json 

from datetime               import datetime, timedelta 

from django.views           import View 
from django.http            import JsonResponse

from .models                import User
from my_settings            import SECRET, ALGORITHM

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        minimun_password = 8
    
        if (User.objects.filter(name=data['name']) or 
            User.objects.filter(email=data['email']) or 
            User.objects.filter(phone_numbers=data['phone_numbers'])):
            return JsonResponse({
                'message':'ALREADY TAKEN'}, status = 400)

        if not ('password' or 'email') in data:
            return JsonResponse({
                'message':'KEY ERROR'}, status = 400)

        if not ('@' and '.') in data['email']:
            return JsonResponse({
                'message':'NOT A VALID EMAIL'}, status = 400)

        if len(data['password']) <= minimun_password:
            return JsonResponse({
                'message':'PASSWORD IS TOO SHORT'}, status = 400)
        
        password = bcrypt.hashpw(
                data['password'].encode('utf-8'), 
                bcrypt.gensalt()).decode('utf-8')
        User(
            name          = data['name'],
            email         = data['email'],
            password      = password,
            phone_numbers = data['phone_numbers']
        ).save()

        return JsonResponse(
            {'message':'SUCCESS'}, status = 200
        )

    def get(self, request):
        user_data = User.objects.values()
        return JsonResponse(
            {'users':list(user_data)}, status = 200
        )

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
    
        if not ('password' or 'name') in data:
            return JsonResponse({
                'message':'KEY ERROR'}, status = 400)

        if User.objects.filter(name = data['name']).exists():
            user = User.objects.get(name = data['name'])
            password = data['password'].encode('utf-8')
           
            if bcrypt.checkpw(password, user.password.encode('utf-8')):
                token = jwt.encode(
                    {'user_id': user.id}, SECRET, algorithm = ALGORITHM).decode('utf-8')
    
                return JsonResponse({
                    'Authorized' : token}, status = 200) 
            return JsonResponse({
                'message' : 'Unauthorized'}, status = 401)
        return JsonResponse({
            'message':'INVALID_USER'}, status = 401)  
