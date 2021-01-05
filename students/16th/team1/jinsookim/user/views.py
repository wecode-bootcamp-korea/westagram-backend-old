import re
import jwt
import json
import bcrypt
from westagram.settings import SECRET
from django.views import View 
from .models import Users, Follow
from django.http import JsonResponse
from django.db.models import Q
from user.utils import login_decorator


# Create your views here.
class Sign_Up(View):
    def post(self, request):
        data         = json.loads(request.body)
        LEN_PASSWORD = 8
        
        phone_number = data.get("phone_number")
        user_name    = data.get("user_name")
        email        = data.get("email")
        password     = data.get("password")

        try:    
            if not email and not phone_number and not user_name:
                return JsonResponse({'MESSAGE': 'KEY_ERRORS'}, status=400)

            if not password:
                return JsonResponse({'MESSAGE': 'KEY_ERRORS'}, status=400)

            if len(password) < LEN_PASSWORD:
                return JsonResponse({"message" :"비밀번호를 8자리 이상 입력해주세요."}, status = 400)

            if user_name:
                if Users.objects.filter(user_name = user_name).exists():
                    return JsonResponse({"message" :"이미 회원가입 되어있습니다."}, status = 400)

            if email:
                email_compile = re.compile("\w+\@[a-zA-Z]+\.[a-zA-Z]+")
                email_check   = email_compile.match(email)   
                if not email_check:
                    return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=400)
                if Users.objects.filter(email = email).exists():
                    return JsonResponse({"message" :"이미 회원가입 되어있습니다."}, status = 400)
                
            if phone_number:
                if Users.objects.filter(phone_number = phone_number).exists():
                    return JsonResponse({"message" :"이미 회원가입 되어있습니다."}, status = 400)

            Users.objects.create(phone_number = phone_number,
                                user_name     = user_name,
                                email         = email,
                                password      = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                                )

            return JsonResponse({"message" :"SUCCESS"}, status = 200)

        except KeyError as e:
            return JsonResponse({"message" : e.args[0]}, status = 400)

        
        
class Sign_in(View):
    def post(self, request):
        data  = json.loads(request.body)
        try:
            account  = data['account']
            new_password = data['password']
            if Users.objects.filter(Q(user_name=account) | Q(phone_number=account)|Q(email =account)).exists()==True:
                user = Users.objects.filter(Q(user_name=account) | Q(phone_number=account)|Q(email =account))
                
                if bcrypt.checkpw(new_password.encode('utf-8'),user[0].password):
                    access_token_id = user[0].id
                    access_token = jwt.encode({'id' : access_token_id}, SECRET, algorithm='HS256')
                    return JsonResponse( {"ACCESS_TOKEN": access_token}, status = 200)
            
            return JsonResponse({"message": "INVALID_USER"}, status = 401) 

        except KeyError as e:
            return JsonResponse({"message" : e.args[0]}, status = 400)


class FollowView(View):
    @login_decorator
    def post(self, request):
        data     = json.loads(request.body)
        follower = Users.objects.get(id = data["follower_id"])
        followee = Users.objects.get(id = data["followee_id"])
        if Follow.objects.filter(follower = follower, followee = followee).exists():
            return JsonResponse({"message" : "UNFOLLOWED"}, status=200)
        follow = Follow(
            follower = follower,
            followee = followee
        )
        follow.save()
        return JsonResponse({"message" : "FOLLOWED"}, status=200)
        
            
