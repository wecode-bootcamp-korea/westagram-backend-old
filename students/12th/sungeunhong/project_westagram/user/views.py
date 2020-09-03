import json 

from django.views import View
from django.http  import JsonResponse
from user.models  import User

class AccountView(View):
    def post(self,request):
        data = json.loads(request.body)
       
        try :
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
                                   
    
# class loginView(View):
#     def post(self,request):
#         data = json.loads(request.body)
        
        # try:
        #     if User.objects.filter(email=data['email']).exist():
        #         login_user = User.objects.get(email=data['email'])

        #         if login_user.password == data['password']:
        #             return JsonResponse({'message':'SUCCESS'}, status=200)

        #         return JsonResponse({'message':'INVALID_PASSWORD OR EMAIL'}, status =400)
            
        # except KeyError:   
        #     return JsonResponse(
        #         {'message': 'KEY_ERROR'},
        #         status = 400
        #         )