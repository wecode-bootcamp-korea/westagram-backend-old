import json 

from django.views import View
from django.http  import JsonResponse
from .models      import Users

class Account(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            if data['name'].exist():
                return JsonResponse(
                    {'message': 'ALREADY_EXISTS'},
                    status = 400
                    )
            if data['phone_number'].exist():
                return JsonResponse(
                    {'message': 'ALREADY_EXISTS'},
                    status = 400
                    )
            if data['email'].exist():
                return JsonResponse(
                    {'message': 'ALREADY_EXISTS'},
                    status = 400
                    ) 
            
            if not '@' in data['email'] or not '.' in data['email']:
                return JsonResponse(
                    {"message": "INVALID_EMAIL"}, 
                    status = 400
                    )
            if len(data['password']) < 8:
                return JsonResponse(
                    {"message": "Password must be at least 8 digits."},
                    status = 400
                    )
            
            Users(
                name         = data['name'],
                phone_number = data['phone_number'],
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
                                   
    