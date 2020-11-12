import json
import re
import bcrypt
import jwt

from django.http import JsonResponse
from django.views import View
from django.db.models import Q

from user.models import User, Follow
from user.utils import login_check
from my_db_settings import SECRET_KEY, ALGORITHM

class UsersView(View):

    def post(self, request):
        data           = json.loads(request.body)
        valid_email_re = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

        try:
            new_name        = data['name']
            new_email       = data['email']
            new_password    = data['password']
            new_phone       = data['phone']
        except KeyError:
            return JsonResponse({'message': "KEY_ERROR"}, status = 400)

        #email validation
#        if '@' in new_email and '.' in new_email.split('@')[1]:
#            valid_email = True
#        else:
#            return JsonResponse({'message': "Invalid Email"}, status = 400)

        #email validation using re
        if not re.search(valid_email_re, new_email):
            return JsonResponse({'message': "Invalid Email"}, status = 400)

        if new_name.isspace():
            return JsonResponse({'message': "INVALID_NAME"}, status = 400)

        #password validation
        if not len(new_password) >= 8:
            return JsonResponse({'message': "Invalid Password"}, status = 400)

        #duplacted value validation
        exist_user = User.objects.filter(Q(name=new_name) | Q(phone=new_phone) | Q(email=new_email))
        if exist_user:
            return JsonResponse({'message': "Name, Phone or Email is already exists"}, status = 400)

        try:
            new_profile_pic = data['profile_image']
        except KeyError:
            new_profile_pic = ''

        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User.objects.create(
            name          = new_name,
            email         = new_email,
            phone         = new_phone,
            profile_image = new_profile_pic,
            password      = hashed_password,
        )

        return JsonResponse({'message': "SUCCESS"}, status = 200)

class LoginView(View):

    def post(self, request):
        data           = json.loads(request.body)
        valid_email_re = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'

        try:
            input_account  = data['account']
            input_password = data['password'].encode('utf-8')
        except Exception as error_msg:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

        try:
            user = User.objects.get(Q(name=input_account)|Q(email=input_account)|Q(phone=input_account))
        except Exception:
            return JsonResponse({'message': 'INVALID_USER'}, status = 400)

        if bcrypt.checkpw(input_password,user.password.encode('utf-8')):
            SECRET = SECRET_KEY
            access_token = jwt.encode({'id':user.id}, SECRET, algorithm=ALGORITHM)

            return JsonResponse({'message': 'SUCCESS',
                                 'access_token': access_token.decode('utf-8')}, status = 200)

        return JsonResponse({'message': 'INVALID PASSWORD OR ACCOUNT'}, status = 400)

class FollowView(View):
    @login_check
    def post(self, request):
        user_id = request.user.id
        followee_id = request.GET.get('followee')

        if not followee_id:
            return JsonResponse({'message': 'Check Querystring'}, status = 400)
        try:
            user     = User.objects.get(id=user_id)
            followee = User.objects.get(id=followee_id)
        except Exception:
            return JsonResponse({'message': 'INVALID_USER'}, status = 400)

        Follow(
            follower = user,
            followee = followee,
        ).save()

        return JsonResponse({'message': 'SUCCESS'}, status = 400)
