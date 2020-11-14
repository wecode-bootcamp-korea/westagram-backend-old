import json
import re
import bcrypt
import jwt

from django.db.models import Q
from django.http      import JsonResponse
from django.views     import View

import my_settings
from .models          import User
from core.utils       import (validate_email,
                              validate_password,
                              validate_phone_number,
                              login_decorator)

class Register(View):

    def post(self, request):
        data = json.loads(request.body)
        if not validate_email(data['email']):
            return JsonResponse({'message':'INVALID_MAIL'}, status = 400)
        if not validate_password(data['password']):
            return JsonResponse({'message':'INVALID_PASSWORD'}, status = 400)
        if not validate_phone_number(data['phone_number']):
            return JsonResponse({'message':'INVALID_PHONE_NUMBER'}, status = 400)
        try:
            if User.objects.filter(Q(username= data['username']) | Q(email = data['email']) | Q(phone_number = data['phone_number'])):
                return JsonResponse({'message': 'USER ALREADY EXIST'}, status = 400)
            password        = data['password']
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cryped_password = hashed_password.decode('utf-8')

            User.objects.create(
                username     = data['username'],
                email        = data['email'],
                password     = cryped_password,
                phone_number = data['phone_number']
            )
            return JsonResponse({'message':'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'meesge':'KEY_ERROR'}, status =400)

class LogIn(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user = User.objects.filter(Q(username=data['key']) | Q(email=data['key']) | Q(phone_number=data['key']))

            # decryped user password and compare with database
            if bcrypt.checkpw(data['password'].encode('utf-8'), user[0].password.encode('utf-8')):
                # if Ture, issue JWT token
                secret       = my_settings.SECRET_KEY
                token        = jwt.encode({'id': user[0].id}, secret, my_settings.ALGORITHM)
                access_token = token.decode('utf-8')
                context = {
                    'access_token' : access_token,
                    'username'     : data['key']
                }
                return JsonResponse({'result':context}, status = 200)
            return JsonResponse({'meesage': 'INVALID_PASSWORD'}, status = 400)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)
        except UnboundLocalError:
            return JsonResponse({'message':'INVALID_USER'}, status = 400)


class ProfileView(View):
    @login_decorator
    def get(self, request, username):
        try:
            user_id = request.user.id
            user = User.objects.prefetch_related('post_set', 'follow_set').get(id=user_id)
            context = {
                'num_post'   : user.post_set.count(),
                'email'      : user.email,
                'created_at' : str(user.created_at),
                'username'   : user.username,
                'following'  : user.follow_set.filter(follower_id=user_id).exists(),
                'follower'   : user.follow_set.filter(followee_id=user_id).exists(),
                'posts':[
                    {
                        'title'      : post.title,
                        'author'     : post.author.username,
                        'created_at' : post.created_at,
                    }
                    for post in user.post_set.all()
                ]
            }
            return JsonResponse({'result': context}, status=200)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


