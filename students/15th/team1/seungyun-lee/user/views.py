import json
import bcrypt
import jwt

from django.views     import View
from django.http      import JsonResponse
from django.shortcuts import render

from .models     import User
from my_settings import SECRET


class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)
        login_info = list(data.keys())

        for i in login_info:
            if i != 'password':
                login_name = i

        try:        
            if login_name == 'username':
                if User.objects.filter(username=data['username']).exists():
                    raise ValueError 
                print('help')
                if data.get('username') == '' or data.get('password') == '':
                    print(username, password)
                    raise KeyError
            elif login_name == 'email':                
                if data['email'] != '': #email validation
                    symbols_set = '@.'
                    for i in symbols_set:
                        if i not in data['email'] :
                            raise ValueError
                if User.objects.filter(username=data['email']).exists():
                    raise ValueError 
                if data['email'] == '' or data['password'] == '':
                    raise KeyError
            elif login_name == 'phonenumber':
                if User.objects.filter(username=data['phonenumber']).exists():
                    raise ValueError 
                if data['phonenumber'] == '' or data['password'] == '':
                    raise KeyError


            password         = data['password']
            hashed_passwords = User.objects.values_list('password', flat=True).distinct()

            for i in hashed_passwords:
                if bcrypt.checkpw(password.encode('utf-8'), i.encode('utf-8')):
                    raise ValueError

            if len(data['password']) < 8: #password validation
                raise ValueError 
            
            password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

            User.objects.create(
                username    = data.get('username'),
                email       = data.get('email'), 
                phonenumber = data.get('phonenumber'), 
                password    = password.decode('utf-8')
                )
            return JsonResponse({'message': 'SUCCESS'}, status = 200)
    

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'message' : 'Invalid user/password'}, status = 400)

class SigninView(View):
    def post(self, request):
        data       = json.loads(request.body)
        login_info = list(data.keys())

        try:
            if 'password' not in login_info and len(login_info) < 2:
                raise KeyError

            for i in login_info:
                if i != 'password':
                    login_name = i
            
            password = data['password']
            if login_name == 'username':
                hashed_password = User.objects.get(username=data[login_name])
                user_data       = User.objects.get(username=data[login_name])
            elif login_name == 'email':
                hashed_password = User.objects.get(email=data[login_name])
                user_data       = User.objects.get(email=data[login_name])
            elif login_name == 'phonenumber':
                hashed_password = User.objects.get(phonenumber=data[login_name])
                user_data       = User.objects.get(phonenumber=data[login_name])
            
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.password.encode('utf-8')) == False:
                raise ValueError

            id_token = jwt.encode({'id' : user_data.id}, SECRET, algorithm = "HS256")
            id_token = id_token.decode('utf-8')
            return JsonResponse({'token' : id_token}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'message' : 'INVALID_USER'}, status = 401)



