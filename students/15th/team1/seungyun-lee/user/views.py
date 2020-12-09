from django.shortcuts import render

# Create your views here.
import json

from django.views import View
from django.http  import JsonResponse

from .models import User

import bcrypt

class UserView(View):
    def post(self, request):
        data = json.loads(request.body)

        database_contents = User.objects.all()
        print(database_contents)

        try:
            if (data['username'] == '' and data['email'] == '' and data['phonenumber'] == '') or data['password'] == '':
                raise KeyError
            
            if User.objects.filter(username=data['username'], email=data['email'], phonenumber=data['phonenumber'], password=data['password']).exists():
                raise ValueError

            if len(data['password']) < 8: #password validation
                raise ValueError

            if 'email' in data:
                if data['email'] != '': #email validation
                    symbols_set = '@.'
                    for i in symbols_set:
                        if i not in data['email'] :
                            raise ValueError
            
            User.objects.create(
                username= data['username'], 
                email= data['email'], 
                phonenumber = data['phonenumber'], 
                password    = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
                )
            return JsonResponse({'message': 'SUCCESS'}, status = 200)
    
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 423)
        except ValueError:
            return JsonResponse({'message' : 'INVALID USERNAME/EMAIL'}, status = 444)

    
    def get(self, request):
        data = json.loads(request.body)
        user_info = list(data.keys())

        print(user_info)

        try:
            if 'password' not in user_info and len(user_info) < 2:
                raise KeyError
            if User.objects.filter(username=data['username'], email=data['email'], phonenumber=data['phonenumber']).exists() == False:
                raise ValueError

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 423)
        except ValueError:
            return JsonResponse({'message' : 'INVALID USERNAME/EMAIL'}, status = 444)



