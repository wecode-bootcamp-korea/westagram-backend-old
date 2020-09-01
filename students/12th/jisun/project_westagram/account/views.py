import json 

from django.views           import View 
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from .models                import Users

class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)
    
        if Users.objects.filter(name=data['name']) or Users.objects.filter(email=data['email']) or Users.objects.filter(phone_numbers=data['phone_numbers']):
            return JsonResponse({
                'message':'ALREADY TAKEN'}, status = 400)

        if not ('password' or 'phone_numbers') in data:
            return JsonResponse({
                'message':'KEY ERROR'}, status = 400)

        if not ('@' and '.') in data['email']:
            return JsonResponse({
                'message':'NOT A VALID EMAIL'}, status = 400)

        if len(data['password']) <= 8:
            return JsonResponse({
                'message':'PASSWORD IS TOO SHORT'}, status = 400)

        Users(
            name          = data['name'],
            email         = data['email'],
            password      = data['password'],
            phone_numbers = data['phone_numbers']
        ).save()

        return JsonResponse(
            {'message':'SUCCESS'}, status = 200
        )

    def get(self, request):
        user_data = Users.objects.values()
        return JsonResponse(
            {'users':list(user_data)}, status = 200
        )