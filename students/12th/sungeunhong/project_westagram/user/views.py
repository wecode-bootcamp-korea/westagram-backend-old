import json 

from django.views import View
from django.http import JsonResponse
from .models import Users

class Account(view):
    def post(self,request):
        data = json.loads(request.body)
        
        try:
            Users(
                name         = data['name'],
                phone_number = data['phone_number'],
                email        = data['email'],
                password     = data['password']
            )
        
            if Users.filter(name = data['name']).exist():
                return JsonResponse({'message': 'ALREADY_EXISTS'},status = 400)
            elif Users.filter(phone_number = data['phone_number']).exist():
                return JsonResponse({'message': 'ALREADY_EXISTS'},status = 400)
            elif Users.filter(eamil = data['email']).exist():
                return JsonResponse({'message': 'ALREADY_EXISTS'},status = 400) 
            elif not '@' in email or not '.' in email:
                return JsonResponse({"message": "INVALID_EMAIL"}, status = 400)
            elif len(data['password']) < 8:
                return JsonResponse({"message": "Password must be at least 8 digits."},status = 400)
            
            Users.save()
            return JsonResponse({'message': 'SUCCESS'}, status = 200) 
        
        except KeyError:   
            return JsonResponse({'message': 'KEY_ERROR'},status = 400)
                                   
    