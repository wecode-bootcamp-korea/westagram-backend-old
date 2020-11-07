import json

from django.views import View
from django.db.models import Q
from django.http import JsonResponse

from user.models import User
from user.const import NONE, PASSWORD_LEN
from user.validations import Validation
from user.exceptions import (
    BlankFieldException,
    EmailValidException,
    PhoneNumValidException,
    AlreadyExistException,
    PasswordValidException
)

class SignUpIndexView(View):
    
    def get(self, request):
        return JsonResponse({"get": "user_index"}, status=200)

class SignUpView(View):
    def get(self, request):
        return JsonResponse({"get": "user_signup"}, status=200)
    
    def post(self, request):
        data = json.loads(request.body)
        try:
            email     = data["email"]
            phone     = data["phone"]
            name      = data["name"]
            user_name = data["user_name"]
            password  = data["password"]
            
            for key, value in dict(data).items():
                if key == "email" or key == "phone":
                    continue
                
                if value.strip() == "" or value == NONE:
                    raise BlankFieldException
            
            signup_key_email = False
            if email.strip() == "" and phone.strip() == "":
                raise BlankFieldException
            elif email.strip() != "" and phone.strip() == "":
                signup_key_email = True
            elif email.strip() == "" and phone.strip() != "":
                signup_key_email = False
            
            if signup_key_email:
                
                if not Validation.is_valid_email(email):
                    raise EmailValidException
            else:
                if not Validation.is_valid_phone_number(phone):
                    raise PhoneNumValidException
            
            # TODO REGEX_PASSWORD CHECK
            if len(password) < PASSWORD_LEN:
                raise PasswordValidException
            
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
        
        except EmailValidException as e:
            return JsonResponse({'message': e.__str__()}, status=400)
        
        except PhoneNumValidException as e:
            return JsonResponse({'message': e.__str__()}, status=400)
        
        except PasswordValidException as e:
            return JsonResponse({'message': e.__str__()}, status=400)
        
        except AlreadyExistException as e:
            return JsonResponse({'message': e.__str__()}, status=400)
        
        User.objects.create(
            email     = email.strip(),
            phone     = phone.strip(),
            name      = name.strip(),
            user_name = user_name.strip(),
            password  = password.strip(),
        )
        
        return JsonResponse({"post": "SUCCESS"}, status=200)

class LoginView(View):
    def get(self, request):
        return JsonResponse({"get": "user_login"}, status=200)
    
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
            
            get_user_result = NONE
            
            if not Validation.is_not_blank(login_info, password):
                raise BlankFieldException
            
            if Validation.is_valid_email(login_info):
                login_keys["email"] = login_info
            
            elif Validation.is_valid_phone_number(login_info):
                login_keys["phone"] = login_info
            
            else:
                login_keys["user_name"] = login_info
            
            for key, value in login_keys.items():
                if key == "email" and value != NONE:
                    get_user_result = User.objects.get(
                        email    = value,
                        password = password
                    )
                    break
                
                elif key == "phone" and value != NONE:
                    get_user_result = User.objects.get(
                        phone    = value,
                        password = password
                    )
                    break
                
                elif key == "user_name" and value != NONE:
                    get_user_result = User.objects.get(
                          user_name = value,
                          password  = password,
                    )
                    break
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER"}, status=400)
        
        except BlankFieldException as e:
            return JsonResponse({"message": e.__str__()}, status=400)
        
        except Exception:
            return JsonResponse({"message": "UNKNOWN_EXCEPTION"}, status=400)
        
        return JsonResponse({"message": "SUCCESS"}, status=200)