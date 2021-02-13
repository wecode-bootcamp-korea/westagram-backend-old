import json
import re
import bcrypt
import jwt
from json.decoder import JSONDecodeError

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q
from my_settings      import SECRET, ALGORITHM

from user.models import User, Follow
from user.utils  import login_decorator

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
                password      = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            )
       
            return JsonResponse({'message':'SUCCESS'}, status=201)
        
        except JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)


class LogInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            login_id = data.get('id', None)
            password = data.get('password', None)

            if not (login_id and password):
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

            if not User.objects.filter(
                    Q(email         = login_id) |
                    Q(mobile_number = login_id) |
                    Q(username      = login_id)
            ).exists():
                return JsonResponse({'message': 'INVALID_USER'}, status=401)

            user = User.objects.get(
                    Q(email         = login_id) |
                    Q(mobile_number = login_id) |
                    Q(username      = login_id)
            )

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)

            access_token = jwt.encode({"id":user.id}, SECRET, algorithm=ALGORITHM)

            return JsonResponse({'message': 'SUCCESS', 'Authorization':access_token}, status=201)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)


class FollowView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            follower = request.user

            following_id = data.get('following_id', None)

            if not following_id:
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

            if not User.objects.filter(id=following_id).exists():
                return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, status=401)

            following = User.objects.get(id=following_id)

            if Follow.objects.filter(follower=follower, following=following).exists():
                Follow.objects.filter(follower=follower, following=following).delete()
                return JsonResponse({'message': 'SUCCESS'}, status=200)

            Follow.objects.create(
                follower  = follower,
                following = following
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)