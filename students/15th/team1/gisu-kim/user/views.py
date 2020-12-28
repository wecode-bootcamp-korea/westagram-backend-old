import json, re
import bcrypt
import jwt

from django.http      import JsonResponse
from django.views     import View

from .models          import Users

# Create your views here.

class SignUpView(View) : 
    def post(self, request) :
        data = json.loads(request.body)

        #password 암호화
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        
        #email, password 유효성
        email_validation    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        pw_validation       = '^[A-Za-z0-9@#$%^&+=]{8,}$'

        try : 
            if not re.match(email_validation, data['email']) : 
                return JsonResponse(
                        {'message' : 'INVALID_ID'}, status = 401
                        )
            if not re.match(pw_validation, data['password']) : 
                return JsonResponse(
                        {'message' : 'INVALID_PASSWORD'}, status = 401
                        )
            if Users.objects.filter(email=data['email']).exists() : 
                return JsonResponse(
                        {'message' : 'ALREADY_EXISTS'}, status = 401
                        )
            else :
                Users.objects.create(
                        email       = data['email'],
                        password    = hashed_password.decode('utf-8')
                        )
          
                return JsonResponse(
                        {'message' : 'SUCCESS'}, status = 201
                        )

        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

class SignInView(View) : 
    def post(self, request) : 
        data            = json.loads(request.body)
        SECRET          = 'westagram'

        try :
            data['email']   = data.get('email')
            user_password   = data.get('password')

            if Users.objects.filter(email = data['email']).exists() : 
                user = Users.objects.get(email = data.get('email'))
                if bcrypt.checkpw(user_password.encode('utf-8'), user.password.encode('utf-8')):
                    access_token = jwt.encode({'email': data['email']}, SECRET, algorithm = 'HS256').decode('utf-8')
                    return JsonResponse(
                            {'message': "SUCCESS", 'Token' : access_token}, status=200
                            )
                return JsonResponse(
                        {'message' : "PASSWORD_IS_NOT_VALID"}, status = 400
                        )
            else : 
                return JsonResponse({'message' : "THIS_USER_DOES_NOT_EXIST"}, status = 401
                        )
            
        except KeyError : 
            return JsonResponse(
                    {'MESSAGE': "KEY_ERROR"},status=400
                    )
