import json
import re
import bcrypt
import jwt

from django.http      import JsonResponse, HttpResponse
from django.views     import View
from django.db.models import Q

from user.models   import (
    User,
    Follow
)
from westagram.my_settings import SECRET_KEY, ALGORITHM

email_regex              = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
password_regex           = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
phone_regex              = re.compile(r'[0-9]{3}-[0-9]{4}-[0-9]{4}')
MINIMUM_PASSWORD_LENGTH  = 8

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            name                     = data['name']
            phone                    = data['phone']
            email                    = data['email']
            password                 = data['password']
            username                 = data['username']

            if name == "":
                return JsonResponse({"message" : "NAME_REQUIRED"}, status=400)

            if phone == "" and email == "":
                return JsonResponse({"message" : "EMAIL_OR_PHONE_NUMBER_REQUIRED"}, status=400)

            if username == "":
                return JsonResponse({"message" : "USERNAME_REQUIRED"}, status=400)

            if password == "":
                return JsonResponse({"message" : "PASSWORD_REQUIRED"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "EMAIL_EXISTS"}, status=400)
                
            if User.objects.filter(username=username).exists():
                return JsonResponse({"message" : "USERNAME_EXISTS"}, status=400)

            if not email_regex.search(email):
                return JsonResponse({"message" : "EMAIL_VALIDATION"}, status=400)

            if not password_regex.match(password):
                return JsonResponse({"message" : "PASSWORD_VALIDATION"}, status=400)

            if not phone_regex.match(phone):
                return JsonResponse({"message" : "PHONE_VALIDATION"}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') 
                
            User.objects.create(
                name     = name, 
                email    = email, 
                phone    = phone,
                password = hashed_password, 
                username = username
            )

            return JsonResponse({"message" : "SUCCESS"}, status=200)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)


class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            email       = data.get('email', None)
            phone       = data.get('phone', None)
            username    = data.get('username', None)
            password    = data.get('password', None)

            if not ((email or username or phone) and password):
                return JsonResponse({"message" : "REQUIRED_FIELD"}, status=400)

            if User.objects.filter(Q(email=email) | Q(phone=phone) | Q(username=username)): 
                user = User.objects.get(Q(email=email) | Q(phone=phone) | Q(username=username))
                    
                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    access_token = jwt.encode({'user' : user.id}, SECRET_KEY, algorithm=ALGORITHM)
                    return JsonResponse({"message" : "SUCCESS", "TOKEN" : access_token}, status=200)

                return JsonResponse({"message" : "UNAUTHORIZED_APPROACH"}, status=401)

            return JsonResponse({"message" : "INVALID_USER"}, status=401)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400).decode("UTF-8")

class FollowView(View):
    def post(self, request):
        data = json.loads(request.body)
        # try:
        follower     = data['follower']
        following    = data['following']

        follower_id  = User.objects.get(id=follower)
        following_id = User.objects.get(id=following)

        if not follower:
            return JsonResponse({"message" : "INVALID_USER"}, status=400)

        if not following:
            return JsonResponse({"message" : "INVALID_APPROACH"}, status=400)
        
        # Unfollow
        if Follow.objects.filter(follower=follower_id, following=following_id).exists(): #boolean으로 알려준다
            Follow.objects.filter(follower=follower_id, following=following_id).delete()
            return JsonResponse({"message" : "DELETE_SUCCESS"}, status=200)
        
        # Follow
        Follow.objects.create(
                    follower = follower_id,
                    following = following_id
        )
        return JsonResponse({"message" : "CREATE_SUCCESS"}, status=200)
