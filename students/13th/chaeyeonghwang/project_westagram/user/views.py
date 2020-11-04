import json
import bcrypt
import jwt
import re

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from user.models      import User
from user.utils       import LoginConfirm



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
            data            = json.loads(request.body)
            given_pw        = data['password'].encode('utf-8')
            accessing_user  = User.objects.get(Q(email = data['user_input']) | Q(mobile = data['user_input']) | Q(username = data['user_input']))
           
            sucess_msg      = JsonResponse({'MESSAGE':'SUCCESS',
                                            'AUTHORIZATION':jwt.encode({'id' : accessing_user.id}, 'SECRET', algorithm = 'HS256').decode()},
                                            status=200)
            password_msg    = JsonResponse({'MESSAGE':'INCORRECT PASSWORD'},status=401)

            if accessing_user:
                if bcrypt.checkpw( given_pw , accessing_user.password.encode('utf-8') ):
                    return sucess_msg
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