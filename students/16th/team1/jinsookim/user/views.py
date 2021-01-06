import re
import jwt
import bcrypt

import json

from django.views import View 
from django.http import JsonResponse

from .models import Users, Follow
from user.utils import login_decorator
from westagram.settings import SECRET

# Create your views here.
class SignUp(View):
    def post(self, request):
        data         = json.loads(request.body)
        LEN_PASSWORD = 8
        try:
            phone_number = data.get("phone_number")
            user_name    = data.get("user_name")
            email        = data["email"]
            password     = data["password"]

           
            if not email:
                return JsonResponse({"message" :"이메일를 입력해주세요"}, status = 400)

            if len(password) < LEN_PASSWORD:
                return JsonResponse({"message" :"비밀번호를 8자리 이상 입력해주세요."}, status = 400)
    
            if email:
                email_compile = re.compile("\w+\@[a-zA-Z]+\.[a-zA-Z]+")
                email_check   = email_compile.match(email)   

                if not email_check:
                    return JsonResponse({'MESSAGE': 'INVALID_EMAIL'}, status=400)

                if Users.objects.filter(email = email).exists():
                    return JsonResponse({"message" :"이미 회원가입 되어있습니다."}, status = 400)
                
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            Users.objects.create(phone_number = phone_number,
                                user_name     = user_name,
                                email         = email,
                                password      = password.decode('utf-8')
                                )

            return JsonResponse({"message" :"SUCCESS"}, status = 200)

        except KeyError as e:
            return JsonResponse({"message" : e.args[0] + " keyerror"}, status = 400)

        
        
class Signin(View):
    def post(self, request):
        data  = json.loads(request.body)
        try:
            account  = data['account']
            password = data['password']

            if not account:
                return JsonResponse({"message": "이메일 입력해주세요"}, status = 400) 

            if not password:
                return JsonResponse({"message": "패스워드 입력해주세요"}, status = 400) 

            if Users.objects.get(email = account):
                user =  Users.objects.get(email = account)

                if bcrypt.checkpw(password.encode('utf-8'),user.password.encode('utf-8')):
                    access_token_id = user.id
                    access_token    = jwt.encode({'id' : access_token_id}, SECRET, algorithm='HS256')
                    return JsonResponse( {"ACCESS_TOKEN": access_token}, status = 200)
                return JsonResponse( {"message" : "비밀번호가 틀렸습니다"}, status = 400)
            
            
        except KeyError as e:
            return JsonResponse({"message" : e.args[0] + " keyerror"}, status = 400)

        except Users.DoesNotExist:
            return JsonResponse({"message": "이메일이 틀렸습니다."}, status = 401) 

class FollowView(View):
    @login_decorator
    def post(self, request, follower_id):
  
        token    = request.headers.get("Authorization")
        jwt_user = jwt.decode(token, SECRET, algorithms="HS256")

        follower = Users.objects.get(id = follower_id)
        followee = Users.objects.get(id = jwt_user["id"])
        
        if followee.id == follower_id:
            return JsonResponse({"message" : "자신의 계정을 follow 할 수 없습니다."}, status=400)

        if Follow.objects.filter(follower = follower, followee = followee).exists():
            Follow.objects.filter(follower = follower, followee = followee).delete()
            return JsonResponse({"message" : "UNFOLLOWED"}, status=200)

        follow = Follow(
            follower = follower,
            followee = followee
        )
        follow.save()
        return JsonResponse({"message" : "FOLLOWED"}, status=200)
        
            
