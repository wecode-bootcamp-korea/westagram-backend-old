import json

from django.views import View
from django.db.models import Q
from django.http import JsonResponse

from user.models import User
from user.const import NONE, PASSWORD_LEN
from user.validations import Validation
from user.exceptions import (
    BlankFieldException,
    EmailFormatException,
    PhoneFormatException,
    AlreadyExistException,
    PasswordFormatException,
    AuthenticationException
)
from common_util import authorization

class SignUpView(View):
    
    def get(self, request):
        return JsonResponse({"get": "user_signup"}, status=200)

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
                
                if Validation.is_blank(value.strip()):
                    raise BlankFieldException
            
            signup_key_email = False
            if Validation.is_blank(email, phone):
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
            
            if len(users) > 0:
                raise AlreadyExistException
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        except BlankFieldException as e:
            return JsonResponse({'message': e.__str__()}, status=400)
        
        except EmailFormatException as e:
            return JsonResponse({'message': e.__str__()}, status=400)
        
        except PhoneFormatException as e:
            return JsonResponse({'message': e.__str__()}, status=400)
        
        except PasswordFormatException as e:
            return JsonResponse({'message': e.__str__()}, status=400)
        
        except AlreadyExistException as e:
            return JsonResponse({'message': e.__str__()}, status=400)
        
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
            
            if Validation.is_blank(login_info, password):
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
                raise AuthenticationException
            
            access_token = authorization.get_access_token(get_user.id)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=400)
        
        except BlankFieldException as e:
            return JsonResponse({"message": e.__str__()}, status=400)
        
        except AuthenticationException as e:
            return JsonResponse({"message": e.__str__()}, status=400)
        
        except Exception:
            return JsonResponse({"message": "UNKNOWN_EXCEPTION"}, status=400)
        
        return JsonResponse({
            "message"      : "SUCCESS",
            "access_token" : access_token}, status=200)