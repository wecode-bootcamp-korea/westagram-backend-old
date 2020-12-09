import re
import json
import bcrypt
import jwt

from django.http  import JsonResponse
from django.views import View

from user.models        import User
from westagram.settings import SECRET_KEY

validation = {'email':'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,4}))', 
              'password':'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
              'phonenumber':'/01[01789]\d{3,4}\d{4}/'
             }


class SignUp(View):

    def post(self, request):
        data = json.loads(request.body)
        
        try:
            data_email       = data['account']
            data_name        = ''
            data_phonenumber = ''
            data_password    = data['password']
            
            assert re.match(validation['email'], data_email), "INVALID_EMAIL_FORMAT"
            assert re.match(validation['password'], data_password), "INVALID_PASSWORD_FORMAT"

            hashed_password = bcrypt.hashpw(data_password.encode('utf-8'), bcrypt.gensalt()).decode()

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)

        except AssertionError as e:
            return JsonResponse({"message": f"{e}"}, status = 400)

        account_type_list = [data_email, data_name, data_phonenumber]
 
        for account_type_checker in account_type_list:
            if account_type_checker:
                if User.objects.filter(account = account_type_checker).exists():
                    return JsonResponse({"message": "ALREADY_EXISTS_ACCOUNT"}, status = 400)
                else:
                    user = User.objects.create(account = account_type_checker, password = hashed_password)
                    break
        return JsonResponse({"message": "SUCCESS"}, status = 201)

class SignIn(View):
    def post(self, request):
        users         = User.objects.all()
        data          = json.loads(request.body)
        
        try:
            data_account  = data['account']
            data_password = data['password']

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
 
        try:
            signin_user = User.objects.get(account = data_account)
        except:
            return JsonResponse({"message": "INVALID_USER"}, status = 401)
        
        if bcrypt.checkpw(data_password.encode('utf-8'), signin_user.password.encode('utf-8')):
            access_token = jwt.encode({'user_id': signin_user.id}, SECRET_KEY, algorithm = 'HS256')
            return JsonResponse({"message": "SUCCESS", "Authorization": access_token.decode('utf-8')}, status = 200)
        else:
            return JsonResponse({"message": "INVALID_USER"}, status = 401)



