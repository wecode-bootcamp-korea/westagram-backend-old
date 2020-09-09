import json 
import bcrypt
import jwt

from django.views import View
from django.http  import JsonResponse
from user.models  import User

class AccountView(View):
    def post(self,request):
        data = json.loads(request.body)

        try:
            if data['name'] and data['email'] and data['password']:

                if '@' not in data['email'] or '.' not in data['email']:
                    return JsonResponse(
                        {"message": "INVALID_EMAIL"}, 
                        status = 400
                        )    
                 
                if len(data['password']) < 8:
                    return JsonResponse(
                        {'message': 'Password must be at least 8 digits.'},
                        status = 400
                        )     
                if User.objects.filter(email=data['email']).exists():
                    return JsonResponse(
                        {'message': 'ALREADY_EXISTS'},
                        status = 400
                        )
                if User.objects.filter(email=data['name']).exists():
                    return JsonResponse(
                        {'message': 'ALREADY_EXISTS'},
                        status = 400
                        )
                encoded_password = data['password'].encode('utf-8')
                hashed_password = bcrypt.hashpw(encoded_password,bcrypt.gensalt())
                data['password'] = hashed_password.decode('utf-8') 

            User.objects.create(
                name         = data['name'],
                email        = data['email'],
                password     = data['password']
            ).save()
          
            return JsonResponse(
                {'message': 'SUCCESS'}, 
                status = 200
                )  
        
        except KeyError:   
            return JsonResponse(
                {'message': 'KEY_ERROR'},
                status = 400
                )

class loginView(View):
    def post(self,request):
        data = json.loads(request.body)
        
        try:
            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'),user.password.encode('utf-8')):
                    token = jwt.encode({'email': data['email']},'secret_key', algorithm = "HS256").decode('utf-8')
                                                                                                      
                    return JsonResponse({
                        'message':token},
                         status=200
                         ) 
                 
                return JsonResponse(
                        {'message':'INVALID_PASSWORD'},
                         status=400
                         )
            return JsonResponse(
                        {'message':'INVALID_EMAIL'},
                         status=400
                         )

        except KeyError:   
            return JsonResponse(
                {'message': 'KEY_ERROR'},
                status = 400
                )