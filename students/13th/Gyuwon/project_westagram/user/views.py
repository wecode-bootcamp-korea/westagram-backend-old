import json
import re
import jwt
import bcrypt

from django.db.models import Q
from django.views     import View
from django.http      import JsonResponse
from .models          import User


class SignUpView(View):
    def post(self, request):

        try:
            data            = json.loads(request.body)
            name            = data['name']
            email           = data['email']
            password        = data['password']
            phone_number    = data['phone_number']

            if User.objects.filter(Q(email=email) | Q(name=name) | Q(phone_number=phone_number)).exists():
                return JsonResponse({"message": "Existing user."}, status=409)

            elif re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) == None:
                return JsonResponse({"message":"Email is not valid."}, status=400)
                            
            elif len(password) <= 7:
                return JsonResponse({"message":"Password is not valid."}, status=400)
                
            else:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                decoded_password = hashed_password.decode('utf-8')

                User.objects.create(
                        email        = email,
                        name         = name,
                        password     = decoded_password,
                        phone_number = phone_number
                        )

                return JsonResponse({"message": "SUCCESS!"}, status= 201)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if User.objects.filter(name=data['name']).exists():
                user = User.objects.get(name=data['name'])

                if bcrypt.checkpw(data['password'].encode('utf-8'), (user.password).encode('utf-8')) == True:
                    token = jwt.encode({'id': user.id}, 'SECRET_KEY', algorithm='HS256')
                    decoded_token=token.decode('utf-8')
                    return JsonResponse({'message' : 'SUCCESS', 'token': decoded_token}, status=200)
                else:
                    return JsonResponse({"message": "INVALID_USER"}, status=400)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)