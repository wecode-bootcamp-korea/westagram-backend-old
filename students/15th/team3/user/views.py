from django.shortcuts import render
import re
import json
import bcrypt
import jwt
from django.http     import JsonResponse
from .models   import SignUp
from django.views    import View

class SignUpView(View):


        def post(self, request):
            data = json.loads(request.body)

            data['email'] = data.get('email')
            data['tel'] = data.get('tel')
            data['name'] = data.get('name')



            try:
                 if (data['name'] is not None) or (data['tel'] is not None) or (data['email'] is not None):
                    if data['password'] is not None:

                        if len(data['password']) < 8:
                            return JsonResponse({"message": "your password is dangerous."}, status= 401)

                        if ('@' not in data['email']) or ('.' not in data['email']):
                            return JsonResponse({'message':'its not email format'},status=401)

                        if SignUp.objects.filter(name = data['name']).exists() and SignUp.objects.filter(email = data['email']).exists() and SignUp.objects.filter(tel = data['tel']).exists():
                            return JsonResponse({'message':'your information is already registered.'},status=400)

                        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

                        SignUp(
                            tel=data['tel'],
                            email=data['email'],
                            name=data['name'],
                            password=hashed_password.decode()
                        ).save()
                        return JsonResponse({"message": "SUCCESS"}, status=200)

            except KeyError:
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)



class SignIn(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data.get('email')
        tel = data.get('tel')
        name = data.get('name')
        password = data['password']

        try:
            if SignUp.objects.filter(name=name).exists():
                user = SignUp.objects.get(name=name)
                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    access_token = jwt.encode({'id':user.id},SECRET_KEY, algorithm='HS256')
                    return JsonResponse({'message': 'SUCCESS'}, status=200)
                else:
                    return JsonResponse({'message': 'INVALID_USER'}, status=401)

            if SignUp.objects.filter(email=email).exists():
                user = SignUp.objects.get(email=email)
                if bcrypt.checkpw(password.encode('utf-8'),
                                      user.password.encode('utf-8')):
                    access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256')
                    return JsonResponse({'message': 'SUCCESS'}, status=200)
                else:
                    return JsonResponse({'message': 'INVALID_USER'}, status=401)

            if SignUp.objects.filter(tel=tel).exists():
                user = SignUp.objects.get(tel=tel)
                if bcrypt.checkpw(password.encode('utf-8'),
                                  user.password.encode('utf-8')):
                    access_token = jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256')
                    return JsonResponse({'message': 'SUCCESS'}, status=200)
                else:
                    return JsonResponse({'message': 'INVALID_USER'}, status=401)

        except:
             return JsonResponse ({'message': 'KEY_ERROR'}, status=400)




