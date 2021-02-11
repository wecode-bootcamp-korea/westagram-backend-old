import json
import re
import bcrypt
import jwt

from django.http        import JsonResponse
from django.views       import View
from user.models        import User
from westagram.settings     import SECRET_KEY, ALGORITHM

# sign up
class Signup(View):
    def post(self, request):
        try:
            data        = json.loads(request.body)
            name        = data.get('name')
            password    = data.get('password')
            
            if name:
                if password:
                    if User.objects.filter(name=name).exists():
                        return JsonResponse({'message':'DUPLICATED_USERNAME'}, status=400)
                    if len(password) < 8:
                        return JsonResponse({'message':'TOO_SHORT_PW'}, status=400)
                    
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                    User.objects.create(
                        name        = name,
                        password    = hashed_password.decode('utf-8')
                    )
                    return JsonResponse({'message':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except ValueError:  
            return JsonResponse({'message':'DECODE_ERROR'}, status=400)

# sign in
class Signin(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            name        = data['name']
            password    = data['password']
            
            user_info = User.objects.get(name=name)
            signin_id = user_info.name
            signin_pw = user_info.password.encode('utf-8')
            
            if User.objects.filter(name=name).exists():
                if signin_id == name and bcrypt.checkpw(password.encode('utf-8'), signin_pw):
                    access_token = jwt.encode({'name':name}, SECRET_KEY, algorithm = ALGORITHM).decode('utf-8')
                    return JsonResponse({'message':'SUCCESS', 'access_token':access_token}, status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=401)    
        except ValueError:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        except User.MultipleObjectsReturned:
            return JsonResponse({'message':'MULTIPLE_USERS'}, status=409)