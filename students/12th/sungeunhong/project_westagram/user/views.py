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
                if User.objects.filter(name=data['name']).exists():
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
        
    # def get(self,request):
    #     users = User.objects.all()
    #     user_data =[{
    #         'email': user.emil
    #     } for user in users]
    #     return JsonResponse(
    #         {'users':user_data},
    #         status=200
    #         )

class loginView(View):
    def post(self,request):
        data = json.loads(request.body)
        
        try:
            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])

                if bcrypt.checkpw(data['password'].encode('utf-8'),user.password.encode('utf-8')):
                    token = jwt.encode({'email': data['email']},'secret_key', algorithm = "HS256").decode('utf-8')
                                                                                                      
                    return JsonResponse({
                        'Access_token':token},
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