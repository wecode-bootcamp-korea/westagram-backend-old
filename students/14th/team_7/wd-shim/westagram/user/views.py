import json

from django.views     import View
from django.http      import JsonResponse
from django.db.models import Q

from user.models      import User, Follow
from user.const       import NONE, PASSWORD_LEN
from user.validations import Validation
from user.exceptions  import (
    BlankFieldException,
    EmailFormatException,
    PhoneFormatException,
    AlreadyExistException,
    PasswordFormatException,
    WrongPasswordException
)
from common_util import authorization

class SignUpView(View):
    
    def get(self, request):
        return JsonResponse({"get": "SignUpView"}, status=200)
    
    def post(self, request):
        data = json.loads(request.body)
        try:
            email     = data["email"].strip()
            phone     = data["phone"].strip()
            name      = data["name"].strip()
            user_name = data["user_name"].strip()
            password  = data["password"].strip()
            
            for key, value in dict(data).items():
                if key == "email" or key == "phone":
                    continue
                
                if Validation.is_blank(value):
                    raise BlankFieldException
            
            signup_key_email = False
            if Validation.is_any_blank(email, phone):
                raise BlankFieldException
            elif email != "" and phone == "":
                signup_key_email = True
            elif email == "" and phone != "":
                signup_key_email = False
            
            if signup_key_email:
            
                if not Validation.is_valid_email(email):
                    raise EmailFormatException
            else:
                if not Validation.is_valid_phone_number(phone):
                    raise PhoneFormatException
            
            # TODO REGEX_PASSWORD CHECK
            if len(password) < PASSWORD_LEN:
                raise PasswordFormatException
            
            users = User.objects.filter(
                Q(email=email) |
                Q(phone=phone) |
                Q(user_name=user_name)
            )
            
            if users:
                raise AlreadyExistException
            
        except KeyError as e:
            return JsonResponse({'message': f'KEY_ERROR:{e} Field'}, status=400)
        
        except BlankFieldException as e:
            return JsonResponse({'message': f'{e}'}, status=400)
        
        except EmailFormatException as e:
            return JsonResponse({'message': f'{e}'}, status=400)
        
        except PhoneFormatException as e:
            return JsonResponse({'message': f'{e}'}, status=400)
        
        except PasswordFormatException as e:
            return JsonResponse({'message': f'{e}'}, status=400)
        
        except AlreadyExistException as e:
            return JsonResponse({'message': f'{e}'}, status=400)
        
        User.objects.create(
            email     = email,
            phone     = phone,
            name      = name,
            user_name = user_name,
            password  = authorization.get_hashed_pw(password)
        )
        
        return JsonResponse({"post": "SUCCESS"}, status=200)

class SignInView(View):
    
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            login_info = data['login_key'].strip()
            password   = data['password'].strip()
            
            login_keys = {
                "email"     : NONE,
                "phone"     : NONE,
                "user_name" : NONE,
            }
            
            get_user = NONE
            
            if Validation.is_all_blank(login_info, password):
                raise BlankFieldException
            
            if Validation.is_valid_email(login_info):
                login_keys["email"] = login_info
                
            elif Validation.is_valid_phone_number(login_info):
                login_keys["phone"] = login_info
                
            else:
                login_keys["user_name"] = login_info
            
            for key, value in login_keys.items():
                if key == "email" and value != NONE:
                    get_user = User.objects.get(email=value, is_deleted=0)
                    break
                
                elif key == "phone" and value != NONE:
                    get_user = User.objects.get(phone=value, is_deleted=0)
                    break
                
                elif key == "user_name" and value != NONE:
                    get_user = User.objects.get(user_name=value, is_deleted=0)
                    break
            
            if not Validation.is_valid_password(password, get_user.password):
                raise WrongPasswordException
            
            access_token = authorization.get_access_token(get_user.id)
            
        except KeyError as e:
            return JsonResponse({"message": f"{e}"}, status=400)
        
        except BlankFieldException as e:
            return JsonResponse({"message": f"{e}"}, status=400)
        
        except WrongPasswordException as e:
            return JsonResponse({"message": f"{e}"}, status=400)
        
        except User.DoesNotExist as e:
            return JsonResponse({"message": f"{e}"}, status=400)
        
        return JsonResponse({
            "message"     : "SUCCESS",
            "access_token": access_token}, status=200)

# ========================================================================================
# Follow
class FollowView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user_id = data['user_id']
            follow_id = data['follow_id']
            
            user = User.objects.get(id=user_id, is_deleted=0)
            if not Follow.objects.filter(who=user, follower=follow_id).exists():
                Follow.objects.create(who=user, follower=follow_id)
            else:
                Follow.objects.filter(who=user, follower=follow_id).delete()
            
            #TODO: 팔로우한 사람 정보 화면에 전달 (비동기로 화면에 추가함)
            
        except User.DoesNotExist as e:
            return JsonResponse({"message": f"{e}"}, status=400)
        
        return JsonResponse({"message": "SUCCESS"}, status=200)

class GetFollowList(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user_id = data['user_id']
            
            user = User.objects.get(id=user_id, is_deleted=0)
            
            follow_users = []
            if user:
                follows_list = Follow.objects.only("follower").filter(who=user)
                
                for follow in follows_list:
                    follow_users.append(User.objects.get(id=follow.pk))

            result = {
                "user_name": user.user_name,
                "follow_number": len(follow_users),
                "follow_user": [{
                    "name" : f_user.user_name
                } for f_user in follow_users]
            }
            
        except User.DoesNotExist as e:
            return JsonResponse({"message": f"{e}"}, status=400)
            
        return JsonResponse({"follow_list": result}, status=200)

class GetFollowerList(View):
    def post(self, request):
        pass