import json 

from django.views import View
from django.http import JsonResponse
from .models import Users

class Account(view):
    def post(self,request):
        data = json.loads(request.body)
        
        try:
            account = User(
                name         = data['name'],
                phone_number = data['phone_number'],
                email        = data['email'],
                password     = data['password']
            )
           
            if account_db.filter(name = data['name']).exist():
                return JsonResponse({'message': 'ALREADY_EXISTS',status = 400}
            if account_db.filter(phone_number = data['phone_number']).exist():
                return JsonResponse({'message': 'ALREADY_EXISTS',status = 400}
            if account_db.filter(eamil = data['email']).exist():
                return JsonResponse({'message': 'ALREADY_EXISTS',status = 400} 
            account.save()
            return JsonResponse({'message': 'SUCCESS'}, status = 200) 
        
        except KeyError    
            return JsonResponse({'message': 'KEY_ERROR'},status = 400)
        
        except ValidationError as v :
                                   
    