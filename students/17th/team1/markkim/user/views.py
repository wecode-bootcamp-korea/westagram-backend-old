import json
import bcrypt
import jwt

from django.views          import View
from django.http           import JsonResponse, HttpResponse

from westagram.my_settings import SECRET
from . models              import User, Follower, Following
from posts.models          import Comment, Like, Post
from . utils               import login_decorator

class SignUpView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data['email']
            password     = data['password']
            full_name    = data['full_name']
            phone_number = data['phone_number']
            username     = data['username']
 
            if not email or not password:
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

            if '@' not in email or '.' not in email:
                return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)
            
            if len(password) < 8:
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=400)
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({'message': 'FULL_NAME_ALREADY_EXISTS'}, status=409)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'}, status=409)
            
            if User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'message': 'PHONE_NUMBER_ALREADY_EXISTS'}, status=409)
            
            User.objects.create(
                    full_name    = full_name,
                    email        = email,
                    phone_number = phone_number,
                    username     = username,
                    password     = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    )
        
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if not password or not email:
                return JsonResponse({'message': 'MISSING_FIELD'}, status=400)

            if User.objects.filter(email=email).exists():
                hashed_password = User.objects.get(email=email).password.encode('utf-8')

                if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                    encoded_jwt = jwt.encode({'user-id': User.objects.get(email=email).id}, SECRET, algorithm='HS256')
                    return JsonResponse({'message': 'SUCCESS', 'token': encoded_jwt}, status=200)

                else:
                    return JsonResponse({'message': 'INVALID_USER'}, status=401)

            else:
                return JsonResponse({'message': 'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class FollowView(View):
    @login_decorator
    def post(self, request):
        try:
            data         = json.loads(request.body)
            following_id = data['following_id']
            user_id      = request.user.id

            if Following.objects.filter(following_id=following_id, user_id=user_id).exists():
                Following.objects.get(following_id=following_id, user_id=user_id).delete()
                Follower.objects.get(follower_id=user_id, user_id=following_id).delete()
                return JsonResponse({'message': 'SUCCESS'}, status=200)

            else:
                Following.objects.create(following_id=following_id, user_id=user_id)
                Follower.objects.create(follower_id=user_id, user_id=following_id)
                return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)










