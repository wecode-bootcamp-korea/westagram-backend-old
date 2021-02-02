import json

from django.views import View
from django.http  import JsonResponse, HttpResponse

from . models     import User


class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        phone_number = data.get('phone_number', None)

        if 'email' not in data.keys() or 'password' not in data.keys():
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        if '@' not in data['email'] or '.' not in data['email']:
            return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)
        
        if len(data['password']) < 8:
            return JsonResponse({'message': 'INVALID_PASSWORD'}, status=400)
        
        if (data['full_name'],) in User.objects.values_list('full_name'):
            return JsonResponse({'message': 'FULL_NAME_ALREADY_EXISTS'}, status=409)
        
        if (data['email'],) in User.objects.values_list('email'):
            return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'}, status=409)
        
        if phone_number:
            
            if (int(phone_number),) in User.objects.values_list('phone_number'):
                return JsonResponse({'message': 'PHONE_NUMBER_ALREADY_EXISTS'}, status=409)
        
        User.objects.create(
                full_name    = data['full_name'],
                email        = data['email'],
                phone_number = data['phone_number'],
                username     = data['username'],
                password     = data['password']
                )
        
        return JsonResponse({'message': 'SUCCESS'}, status=200)





