import json
import re
import bcrypt
import jwt

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from django.core            import serializers

from project import my_settings
from .models import User, Follow
from .utils  import validate_token
from .helper import (
    name_overlap,
    phone_number_overlap,
    email_overlap,
    email_validate,
    password_validate
)

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            post_email    = data['email']
            post_password = data['password']
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        if 'phone_number' in data.keys():
            post_phone_number = data['phone_number']
        else:
            post_phone_number = ""

        if 'name' in data.keys():
            post_name = data['name']
        else:
            post_name = ""

        try:
            email_validate(post_email)
            password_validate(post_password)
            phone_number_overlap(post_phone_number)
            name_overlap(post_name)
            email_overlap(post_email)
        except ValidationError as e:
            return JsonResponse({'message':e.message}, status = 400)

        post_password = bcrypt.hashpw(post_password.encode('utf-8'), bcrypt.gensalt())

        User(
            phone_number = post_phone_number,
            name         = post_name,
            email        = post_email,
            password     = post_password.decode('utf-8')
        ).save()

        return JsonResponse({'message':'SUCCESS'}, status=200)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        if not (
            (
            'name'         in data.keys() or
            'email'        in data.keys() or
            'phone_number' in data.keys()
            ) and
            'password'     in data.keys()
        ):
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        if 'name' in data.keys():
            if not User.objects.filter(name = data['name']):
                return JsonResponse({'message':'INVALID_USER'}, status = 401)

            elif bcrypt.checkpw(data['password'].encode('utf-8'), User.objects.get(name = data['name']).password):
                access_token = jwt.encode({'id' : User.objects.get(email = data['email']).id }, my_settings.SECRET_KEY, algorithm = 'HS256')
                return JsonResponse({'access_token':access_token.decode()}, status = 200)

        elif 'email' in data.keys():
            if not User.objects.filter(email = data['email']):
                return JsonResponse({'message':'INVALID_USER'}, status = 401)

            elif bcrypt.checkpw(data['password'].encode('utf-8'), User.objects.get(email = data['email']).password.encode('utf-8')):
                access_token = jwt.encode({'id' : User.objects.get(email = data['email']).id }, my_settings.SECRET_KEY, algorithm = 'HS256')
                return JsonResponse({'access_token':access_token.decode()}, status = 200)

        elif 'phone_number' in data.keys():
            if not User.objects.filter(phone_number = data['phone_number']):
                return JsonResponse({'message':'INVALID_USER'}, status = 401)

            elif bcrypt.checkpw(data['password'].encode('utf-8'), User.objects.get(phone_number = data['phone_number']).password.encode('utf-8')):
                access_token = jwt.encode({'id' : User.objects.get(email = data['email']).id }, my_settings.SECRET_KEY, algorithm = 'HS256')
                return JsonResponse({'access_token':access_token.decode()}, status = 200)

class FollowPost(View):
    @validate_token
    def post(self, request):
        data = json.loads(request.body)

        if 'email' not in data:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        email = data['email']

        obj, created = Follow.objects.get_or_create(
            followed_user  = User.objects.get(email = email),
            following_user = request.user
        )

        if created == False:
            obj.delete()
            return JsonResponse({'message':'SUCCESS UnFollwing'}, status = 200)

        return JsonResponse({'message':'SUCCESS Following'}, status = 200)

class FollowGet(View):
    @validate_token
    def get(self, request):
        data = json.loads(request.body)

        if 'email' not in data:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        email = data['email']

        want_user = User.objects.get(email = email).id

        following_count = Follow.objects.filter(following_user = want_user).count()
        followed_count  = Follow.objects.filter(followed_user = want_user).count()

        return JsonResponse({'Following':following_count, 'Followed':followed_count}, status = 200)
