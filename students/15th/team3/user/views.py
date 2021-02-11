from django.shortcuts import render

import json
import bcrypt
import jwt

from django.http     import JsonResponse
from django.views    import View

from .models   import SignUp


class SignUpView(View):
        def post(self, request):
            data = json.loads(request.body)

            email    = data.get('email')
            tel      = data.get('tel')
            name     = data.get('name')
            password = data['password']

            try:
                 #if (name is not None) or (tel is not None) or (email is not None): 아래 if 문으로 수정
                 if name or tel or email:
                    if password:

                        if len(password) < 8:
                            return JsonResponse({"message": "your password is dangerous."}, status= 401)

                        if ('@' not in email) or ('.' not in email):
                            return JsonResponse({'message':'its not email format'},status=401)

                        if SignUp.objects.filter(name = name).exists() and SignUp.objects.filter(email = email).exists() and SignUp.objects.filter(tel = tel).exists():
                            return JsonResponse({'message':'your information is already registered.'},status=400)

                        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                        SignUp(
                            tel=tel,
                            email=email,
                            name=name,
                            password=hashed_password.decode()
                        ).save()
                        return JsonResponse({"message": "SUCCESS"}, status=200)

            except KeyError:
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class SignIn(View):
    def post(self,request):
        data = json.loads(request.body)

        email    = data.get('email')
        #tel      = data.get('tel')
        #name     = data.get('name')
        #password = data['password']

        try:
            # if SignUp.objects.filter(name=name).exists():
            #     user = SignUp.objects.get(name=name)
            #     if bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
            #         #access_token = jwt.encode({'id':user.id},SECRET_KEY, algorithm='HS256')
            #         return JsonResponse({'message': 'SUCCESS'}, status=200)
            #     else:
            #         return JsonResponse({'message': 'INVALID_USER'}, status=401)

            if SignUp.objects.filter(email=email).exists():
                user = SignUp.objects.get(email=email)
                if bcrypt.checkpw(data['password'].encode('utf-8'),
                                      user.password.encode('utf-8')):
                    SECRET ='secret'
                    token = jwt.encode({'id': user.id}, SECRET, algorithm='HS256')
                    return JsonResponse({'message': 'SUCCESS','access_token':token.decode()}, status=200)
                else:
                    return JsonResponse({'message': 'INVALID_USER'}, status=401)

            # if SignUp.objects.filter(tel=tel).exists():
            #     user = SignUp.objects.get(tel=tel)
            #     if bcrypt.checkpw(data['password'].encode('utf-8'),
            #                       user.password.encode('utf-8')):
            #         #access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256')
            #         return JsonResponse({'message': 'SUCCESS'}, status=200)
            #     else:
            #         return JsonResponse({'message': 'INVALID_USER'}, status=401)

        except:
             return JsonResponse ({'message': 'KEY_ERROR'}, status=400)




