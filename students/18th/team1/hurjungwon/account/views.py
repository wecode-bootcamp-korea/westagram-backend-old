import json
import re
import bcrypt
import jwt

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from .models import User, Follow
from my_settings import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not data.get('user_name'):
                return JsonResponse({'message': 'Type user_name'}, status=400)
            
            if not data.get('password'):
                return JsonResponse({'message': 'Type password'}, status=400)
            
            if not data.get('email'):
                return JsonResponse({'message': 'Type email'}, status=400)
            
            user_name    = data['user_name']
            email        = data['email']
            password     = data['password']
            name         = data.get('name', None)
            phone_number = data.get('phone_number', None)
            
            email_match    = re.match('[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]+', email)
            password_match = re.match('\S{8,}', password)
            
            if not email_match:
                return JsonResponse({'message': 'invalid email'}, status=400)
            
            if not password_match:
                return JsonResponse({'message': 'invalid password'}, status=400)

            if User.objects.filter(user_name = user_name).exists():
                return JsonResponse({'message': 'user_name already exists'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decode_password = hashed_password.decode('utf-8')
            
            User.objects.create(
                user_name    = user_name,
                email        = email,
                password     = decode_password,
                name         = name,
                phone_number = phone_number,
            )

            return JsonResponse({'message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user_name     = data.get('user_name', '')
            phone_number  = data.get('phone_number', '')
            email         = data.get('email', '')
            password      = data['password']
            
            if not (user_name or phone_number or email):
                return JsonResponse({'message': 'Type at least one value'}, status=400)
            
            valid_user = User.objects.get(
                Q(user_name=user_name) | Q(email=email) | Q(phone_number=phone_number)
            )

            encode_password = valid_user.password.encode('utf-8')
            
            if not bcrypt.checkpw(password.encode('utf-8'), encode_password):
                return JsonResponse({'message': 'INVALID USER_PASSWORD'}, status=401)

            playload = {'user-id': valid_user.id}
            token    = jwt.encode(playload, SECRET_KEY, algorithm=ALGORITHM)
            
            return JsonResponse({'message': 'SUCCSESS', 'token': token}, status=200)
            
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID USER_ID'}, status=401)

class FollowView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            from_follow = data.get('from_follow')
            to_follow   = data.get('to_follow')

            User.objects.get(id=to_follow)

            if from_follow == to_follow:
                return JsonResponse({'message': 'CAN NOT FOLLOW YOURSELF'}, status=400)
            
            if Follow.objects.filter(Q(from_follow=from_follow) & Q(to_follow=to_follow)).exists():
                return JsonResponse({'message': 'ALREADY FOLLOWED'}, status=400)

            Follow.objects.create(
                from_follow_id = from_follow,
                to_follow_id   = to_follow, 
            )

            return JsonResponse({'message': 'SUCCSESS'}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID USER_ID'}, status=401)