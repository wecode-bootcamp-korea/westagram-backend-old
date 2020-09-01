import json 

from django.views import View
from django.http  import JsonResponse
from .models      import User

class Account(View):
    def post(self,request):
        data      = json.loads(request.body)
        user_db   = User.objects.all()
        try:
            User(
                name         = data['name'],
                phone_number = data['phone_number'],
                email        = data['email'],
                password     = data['password']
            )
        
            if user_db.filter(name = data['name']).exist():
                return JsonResponse({'message': 'ALREADY_EXISTS'},status = 400)
            elif user_db.filter(phone_number = data['phone_number']).exist():
                return JsonResponse({'message': 'ALREADY_EXISTS'},status = 400)
            elif user_db.filter(eamil = data['email']).exist():
                return JsonResponse({'message': 'ALREADY_EXISTS'},status = 400) 
            elif not '@' in user_db.filter(email = data['email']) or not '.' in user_db.filter(email = data['email']):
                return JsonResponse({"message": "INVALID_EMAIL"}, status = 400)
            elif len(data['password']) < 8:
                return JsonResponse({"message": "Password must be at least 8 digits."},status = 400)
           
            User.save()
            return JsonResponse({'message': 'SUCCESS'}, status = 200) 
        
        except KeyError:   
            return JsonResponse({'message': 'KEY_ERROR'},status = 400)
                                   
    