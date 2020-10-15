import json
import bcrypt
import jwt
import re

from django.http    import JsonResponse
from django.views   import View
from user.models    import User
from user.utils     import LoginConfirm

# Create your views here.

class SignupView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)

            if ('@' not in data['email'] or 
                '.' not in data['email']):
                return JsonResponse(
                    {'MESSAGE': 'Invalid Email'},
                    status=403)
            elif len(data['password']) < 8:
                return JsonResponse(
                    {'MESSEAGE': 'The password length should be greater than 7.'},
                    status=400)
            elif (User.objects.filter(email = data['email']).exists() or 
                User.objects.filter(username = data['username']).exists()):
                return JsonResponse(
                    {'MESSAGE': 'The given information has been already taken.'},
                    status=403)
            else:
                User(
                    mobile      = data['mobile'],
                    email       = data['email'],
                    full_name   = data['full_name'],
                    username    = data['username'],
                    password    = bcrypt.hashpw( data['password'].encode('utf-8'), bcrypt.gensalt() ).decode()  #디코드해서 저장^^..
                ).save()
                

                
                # print(User.objects.get(username = data['username']).password)
                # print(type(User.objects.get(username = data['username']).password))
                return JsonResponse(
                    {'MESSAGE':'REGISTER_SUCCESS'
                    }
                    , status=201)

        except KeyError:
            return JsonResponse(
                {'MESSAGE':'KEY_ERROR'}, 
                status=400)

class LoginView(View):
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            given_pw = data['password'].encode('utf-8')
            password_msg = JsonResponse({'MESSAGE':'PASSWORD INCORRECT'},status=401)



            if 'email' in data.keys():
                if User.objects.filter(email = data['email']).exists():
                    if bcrypt.checkpw( given_pw , User.objects.get(email = data['email']).password.encode('utf-8') ):
                        accessing_user = User.objects.get(email = data['email']).id
                        return JsonResponse({'MESSAGE':'SUCCESS',
                        'AUTHORIZATION':jwt.encode({'id' : accessing_user}, 'SECRET', algorithm = 'HS256').decode()},
                        status=200)
                    else:
                        return password_msg
            elif 'mobile' in data.keys():
                if User.objects.filter(mobile = data['mobile']).exists():
                    if bcrypt.checkpw( given_pw , User.objects.get(mobile = data['mobile']).password.encode('utf-8')):
                        accessing_user = User.objects.get(mobile = data['mobile']).id
                        return JsonResponse({'MESSAGE':'SUCCESS',
                        'AUTHORIZATION':jwt.encode({'id' : accessing_user}, 'SECRET', algorithm = 'HS256').decode()},
                        status=200)
                    else:
                        return password_msg
            elif 'username' in data.keys():
                if User.objects.filter(username = data['username']).exists():
                    if bcrypt.checkpw( given_pw , User.objects.get(username = data['username']).password.encode('utf-8') ):
                        accessing_user = User.objects.get(username = data['username']).id
                        return JsonResponse({'MESSAGE':'SUCCESS',
                        'AUTHORIZATION':jwt.encode({'id' : accessing_user}, 'SECRET', algorithm = 'HS256').decode()},
                        status=200)
                    else:
                        return password_msg

            else:
                return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse(
                {'MESSAGE':'KEY_ERROR'},
                status=400)


class FollowingView(View):
    @LoginConfirm
    def post(self, request):
        data = json.loads(request.body)
        
        if User.objects.filter(id = data['follower'], follow = data['following']).exists():
            unfollow = User.objects.get(id = data['follower'])
            unfollow.follow.remove(data['following'])

            return JsonResponse(
                {'MESSAGE': 'UNFOLLOW'},
                status=200)

        else:
            follower = User.objects.get(id = data['follower'])
            follower.follow.add(data['following'])
        
            return JsonResponse(
                {'MESSAGE':'FOLLOW'},
                status=200)
