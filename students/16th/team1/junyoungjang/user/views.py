import json
import re

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from .exception_check import exception_check
from .models          import User, Follow

class RegisterView(View):
    @exception_check
    def post(self,request):

        try:
            MIN_PASSWORD_LENGTH = 7
            MIN_NICKNAME_LENGTH = 1
            data             = json.loads(request.body)
            name             = data['name']
            phonenumber      = data['phonenumber'].replace("-",'')
            email            = data['email']
            password         = data['password']
            nickname         = data['nickname']
            
            p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            if p.match(email) == None:
                return JsonResponse({'MESSAGE :':"INVAILD_EMAIL_ADDRESS!"},status = 400)

            if not len(password)>MIN_PASSWORD_LENGTH:
                return JsonResponse({'MESSAGE :':f"PASSWORD_MUST_TO_BE_OVER_{MIN_PASSWORD_LENGTH}_DIGITS"},status = 400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE :':"EMAIL_ALREADY_EXISTS!"},status = 400)

            if User.objects.filter(phonenumber=phonenumber).exists():
                return JsonResponse({'MESSAGE :':"PHONENUMBER_ALREADY_EXISTS!"},status = 400)

            if not phonenumber.isdigit():
                return JsonResponse({'MESSAGE :':"PHONENUMBER_SHOULD_CONTAIN_ONLY_DIGITS"},status = 400)

            if User.objects.filter(nickname=nickname).exists():
                return JsonResponse({'MESSAGE :':"NICKNAME_ALREADY_EXISTS!"},status = 400)

            if not len(nickname)>MIN_NICKNAME_LENGTH:
                return JsonResponse({'MESSAGE :':f"NICKNAME_MUST_BE_OVER_{MIN_NICKNAME_LENGTH}_CHARACTERS!"},status = 400)
            
            User.objects.create(
                name        = name,
                phonenumber = phonenumber, 
                email       = email, 
                password    = password,
                nickname    = nickname
            )
            
            return JsonResponse({'MESSAGE :':"SUCCESS "},status = 200)

        except BlankFieldException as e:
            return JsonResponse({'MESSAGE :':e.__str__()},status = 400)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_USER"},status = 400)


class LoginView(View):
    @exception_check
    def post(self,request):

        try:
            data             = json.loads(request.body)
            email            = data['email']
            password         = data['password']
            user_info        = User.objects.get(email=email)

            if user_info.password == password:
                return JsonResponse({'MESSAGE :':"SUCCESS"}, status = 200)
            else:
                return JsonResponse({'MESSAGE :':"INVAILD_USER"},status = 401)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_USER"},status = 401)

class FollowView(View):
    @exception_check
    def post(self, request):
        
        try:
            data            = json.loads(request.body)
            followee        = User.objects.get(id = data['followee'])
            follower        = User.objects.get(id = data['follower'])
            follow_relation = Follow.objects.filter(
                Q(followee=followee) &
                Q(follower=follower)
            )
            if follow_relation.exists():
                follow_relation.delete()
            
                return JsonResponse({'MESSAGE :':f"UNFOLLOWED_{followee.nickname}!"},status = 200)
            Follow.objects.create(followee=followee, follower=follower)

            return JsonResponse({'MESSAGE :':f"FOLLOWED_{followee.nickname}!"},status = 200)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_USER"},status = 401)

    @exception_check           
    def get(self, request):
    
        follows  = Follow.objects.all()
        req_list = []

        for follow in follows:
            req_dict   = {
                'id'       : follow.id,
                'followee' : follow.followee.nickname,
                'follower' : follow.follower.nickname,
            }
            req_list.append(req_dict)
        return JsonResponse({'follows :':req_list},status = 200)
            

                        