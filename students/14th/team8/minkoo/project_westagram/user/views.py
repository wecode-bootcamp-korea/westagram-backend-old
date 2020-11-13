import json
import re

import bcrypt
import jwt

from django.views                        import View
from django.http                         import JsonResponse
from django.db.models                    import Q

from .models                             import User, FollowList
from project_westagram.settings.settings import JWT_SECRET_KEY, JWT_ALGORITHM
from utils                               import login_decorator

class SignUpView(View):
    def post(self, request):
        email_check          = re.compile('^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$')
        password_check       = re.compile(r'^.*(?=.{8,18})(?=.*[a-zA-Z])(?=.*?[A-Z])(?=.*\d)[a-zA-Z0-9!@#£$%^&*()_+={}\-?:~\[\]]+$')
        phone_check          = re.compile('(\d{3})(\d{3,4}\d{4})')
        name_check           = re.compile('^[a-zA-Z0-9]+(([^,. !@#$%^&*()\'\";:<>?\/ = +|`~][a-zA-Z])?[a-zA-Z]*)*$')
        data                 = json.loads(request.body)

        if not 'email' in data or not 'password' in data or not 'name' in data or not 'phone' in data:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        if not re.match(name_check, data['name']) or len(data['name']) > 15 or len(data['name']) < 3:
            return JsonResponse({'message':'BAD_NAME_REQUEST'}, status=400)

        if not re.match(email_check,data['email']):
            return JsonResponse({'message':'BAD_EMAIL_REQUEST'}, status=400)

        if not re.match(password_check,data['password']) or len(data['password']) < 8: 
            return JsonResponse({'message':'BAD_PASSWORD_REQUEST'},status=400)

        if not re.match(phone_check, data['phone']) or len(data['phone']) > 11 or len(data['phone']) < 10:
            return JsonResponse({'message':'BAD_PHONE_NUMBER_REQUEST'}, status=400)

        if User.objects.filter(Q(name=data['name']) | Q(email=data['email']) | Q(phone=data['phone'])):    
            return JsonResponse({'message':'USER_EXISTS'}, status=400)

        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.objects.create(
            name     = data['name'],
            email    = data['email'],
            phone    = data['phone'],
            password = hashed_password,
        )

        return JsonResponse({'message':'SUCCESS'},status=200)
    
class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        if ('name' not in data and 'phone' not in data and 'email' not in data) or ('password' not in data):
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        user_info = [value for key, value in data.items() if key != 'password']
        user = User.objects.filter(Q(name=user_info[0]) | Q(email=user_info[0]) | Q(phone=user_info[0]))

        if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user[0].password.encode('utf-8')):  
            return JsonResponse({'message':'INVALID_USER'}, status=401) 

        access_token = jwt.encode({'user_id':user[0].id}, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM).decode('utf-8')

        return JsonResponse({'access_token':access_token}, status=200)

class FollowView(View):
    @login_decorator
    def post(self, request):
        data    = json.loads(request.body) 
        user_id = request.user_id

        if not user_id or 'follow_id' not in data:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        if not User.objects.filter(id=data['follow_id']).exists():
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        if FollowList.objects.filter(user_id=user_id, follow_user_id=data['follow_id']).exists():
            return JsonResponse({'message':'THIS_USER_ALREADY_FOLLOING'}, status=400)

        FollowList.objects.create(
            user_id = user_id,
            follow_user_id = data['follow_id']
        )
        return JsonResponse({'message':'SUCCESS'}, status=200)
    
    @login_decorator
    def delete(self, request):
        data    = json.loads(request.body)
        user_id = request.user_id

        if not user_id or 'follow_id' not in data:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        if not User.objects.filter(id=data['follow_id']).exists():
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        
        if not FollowList.objects.filter(id=user_id, follow_user_id=data['follow_id']).exists():
            return JsonResponse({'message':'USER_NOT_FOLLOWED'}, status=404)

        delete_follow = FollowList.objects.get(user_id=user_id, follow_user_id=data['follow_id'])
        delete_follow.delete()
        return JsonResponse({'message':'SUCCESS'}, status=200)
