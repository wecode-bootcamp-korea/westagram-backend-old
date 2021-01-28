import json
import re
import jwt
import bcrypt

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from .exception_check import exception_check
from .models          import User, Follow
from my_settings      import JWT_SECRET, SALT

class RegisterView(View):
    def post(self,request):

        try:
            MIN_PASSWORD_LENGTH = 7
            MIN_NICKNAME_LENGTH = 1
            data                = json.loads(request.body)
            name                = data['name']
            phone_number        = data['phonenumber'].replace("-",'')
            email               = data['email']
            password            = data['password']
            nickname            = data['nickname']

            p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            if not p.match(email):
                return JsonResponse({'MESSAGE :':"INVAILD_EMAIL_ADDRESS!"},status = 400)

            if not len(password) > MIN_PASSWORD_LENGTH:
                return JsonResponse({'MESSAGE :':f"PASSWORD_MUST_TO_BE_OVER_{MIN_PASSWORD_LENGTH}_DIGITS"},status = 400)

            if not len(nickname) > MIN_NICKNAME_LENGTH:
                return JsonResponse({'MESSAGE :':f"NICKNAME_MUST_BE_OVER_{MIN_NICKNAME_LENGTH}_CHARACTERS!"},status = 400)

            if User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE :':"EMAIL_ALREADY_EXISTS!"},status = 400)

            if User.objects.filter(phonenumber = phone_number).exists():
                return JsonResponse({'MESSAGE :':"PHONE_NUMBER_ALREADY_EXISTS!"},status = 400)

            if not phone_number.isdigit():
                return JsonResponse({'MESSAGE :':"PHONE_NUMBER_SHOULD_CONTAIN_ONLY_DIGITS"},status = 400)

            if User.objects.filter(nickname=nickname).exists():
                return JsonResponse({'MESSAGE :':"NICKNAME_ALREADY_EXISTS!"},status = 400)

            encoded_password = password.encode('utf-8')
            hashed_password  = bcrypt.hashpw(encoded_password, bcrypt.gensalt()).decode()
            User.objects.create(
                name        = name,
                phonenumber = phone_number, 
                email       = email, 
                password    = hashed_password,
                nickname    = nickname
            )
            return JsonResponse({'MESSAGE :':"SUCCESS "},status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)

        except ValueError:
            return JsonResponse({'MESSAGE :':"VALUE_ERROR"},status = 400)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_USER"},status = 400)

        except BlankFieldException as e:
            return JsonResponse({'MESSAGE :':e.__str__()},status = 400)


class LoginView(View):
    def post(self,request):

        try:
            data            = json.loads(request.body)
            password        = data['password']
            verifiable_list = ['email','nickname','phonenumber'] 
            # email, phone, nickname 셋 중 하나로 로그인 가능 
            verify_info     = {x : data[x] for x in data if x in verifiable_list}

            if not verify_info:
                return JsonResponse({'MESSAGE :':"PLEASE_ENTER_EMAIL_NICKNAME_OR_PHONENUMER"},status = 401)

            user_info = User.objects.get(**verify_info)

            if bcrypt.checkpw(password.encode('utf-8'), user_info.password.encode('utf-8')):
                user_token = jwt.encode({'user_id': user_info.id}, JWT_SECRET, algorithm = "HS256")
                return JsonResponse({'TOKEN :': user_token}, status = 200)
            else:
                return JsonResponse({'MESSAGE :':"CHECK_YOUR_PASSWORD"},status = 401)

        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)

        except ValueError:
            return JsonResponse({'MESSAGE :':"VALUE_ERROR"},status = 400)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_USER"},status = 401)

class FollowView(View):
    def post(self, request):
        
        try:
            data            = json.loads(request.body)
            followee        = User.objects.get(id = data['followee'])
            follower        = User.objects.get(id = data['follower'])
            follow_relation = Follow.objects.filter(
                Q(followee = followee) &
                Q(follower = follower)
            )
            if follow_relation.exists():
                follow_relation.delete()
            
                return JsonResponse({'MESSAGE :':f"UNFOLLOWED_{followee.nickname}!"},status = 200)
            Follow.objects.create(followee=followee, follower=follower)

            return JsonResponse({'MESSAGE :':f"FOLLOWED_{followee.nickname}!"},status = 200)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)

        except ValueError:
            return JsonResponse({'MESSAGE :':"VALUE_ERROR"},status = 400)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE :':"INVAILD_USER"},status = 401)
      
    def get(self, request):
    
        try:
            follows  = Follow.objects.all()
            req_list = []

            for follow in follows:
                req_dict   = {
                    'id'       : follow.id,
                    'followee' : follow.followee.nickname,
                    'follower' : follow.follower.nickname,
                }
                req_list.append(req_dict)
            return JsonResponse({'FOLLOWS :':req_list},status = 200)
        except KeyError:
                    return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)
            

                        