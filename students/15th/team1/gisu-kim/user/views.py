import json
import re
from django.http      import JsonResponse
from django.views     import View

from .models          import Users

# Create your views here.

class SignUpView(View) : 
    def post(self, request) :
        data = json.loads(request.body)

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
                Users(
                    email       = data['email'],
                    password    = data['password']
                    ).save()
                return JsonResponse(
                        {'message' : 'SUCCESS'}, status = 200
                        )

        except KeyError :
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

class SignInView(View) : 
    def post(self, request) : 
        data = json.loads(request.body)

        try : 
            Users.objects.get(
                    email = data['email'], password =data['password']
                    )
            return JsonResponse(
                    {'message': "SUCCESS"}, status=200
                    )

        except KeyError : 
            return JsonResponse(
                    {'MESSAGE': "KEY_ERROR"},status=400
                    )
        
        except Users.DoesNotExist : 
            return JsonResponse(
                    {'MESSAGE': "INVALID_USER"},status=401
                    )
