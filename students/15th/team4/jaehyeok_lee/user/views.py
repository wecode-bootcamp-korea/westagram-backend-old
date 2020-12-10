import re
import json
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View

from user.models        import User
from westagram.settings import SECRET_KEY

REGEX_EMAIL        = '([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,4}))'
REGEX_PASSWORD     = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$'

class SignUp(View):

    def post(self, request):

        try:
            data = json.loads(request.body)

            email       = data.get('email')
            name        = data.get('name')
            phonenumber = data.get('phonenumber')
            password    = data['password']
            
            if not (email or name or phonenumber):
                raise KeyError
            if email:
                assert re.match(REGEX_EMAIL, email), "INVALID_EMAIL_FORMAT"
            assert re.match(REGEX_PASSWORD, password), "INVALID_PASSWORD_FORMAT"

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()
        
        except json.JSONDecodeError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)

        except AssertionError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)

        account_type_list = [email, name, phonenumber]
 
        for account_type_checker in account_type_list:
            if account_type_checker:
                if User.objects.filter(account = account_type_checker):
                    return JsonResponse({"message": "ALREADY_EXISTS_ACCOUNT"}, status = 400)
                else:
                    User.objects.create(account = account_type_checker, password = hashed_password)
                    break
        return JsonResponse({"message": "SUCCESS"}, status = 201)

class SignIn(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            account  = data['account']
            password = data['password']

            signin_user = User.objects.get(account = account)
        
        except json.JSONDecodeError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        
        except User.DoesNotExist:
            return JsonResponse({"message": "INVALID_USER_NAME_OR_PASSWORD"}, status = 400)

        if bcrypt.checkpw(password.encode('utf-8'), signin_user.password.encode('utf-8')):
            access_token = jwt.encode({'user_id': signin_user.id}, SECRET_KEY, algorithm = 'HS256')
            return JsonResponse({"message": "SUCCESS", "Authorization": access_token.decode('utf-8')}, status = 200)
        else:
            return JsonResponse({"message": "INVALID_USER_NAME_OR_PASSWORD"}, status = 401)



