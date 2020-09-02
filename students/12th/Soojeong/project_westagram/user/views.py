import json
from .models import Users
from django.http import JsonResponse
from django.views import View



class SignUpView(View):

    def post(self, request):
        data = json.loads(request.body)
        Users(
        	name		= data['name'],
            	email           = data['email'],
            	phone_number    = data['phone_number'],
            	password        = data['password'],
            	user_name       = data['user_name'],
        ).save()
            
        #if email not in data.keys() or password not in data.keys():
         #   return JsonResponse({'message':'KEY_ERROR'}, status=400)

        #elif "@" not in email or "." not in email:
         #   return JsonResponse({'message':'email address incorrect'}, status=400)
        
        #elif len(password) < 8:
         #   return JsonResponse({'message':'password must be longer than 8 characters'}, status=400)
        
#        signup_user.objects.create()
        return JsonResponse({'message':'SUCCESS'}, status=200)


"""
            기존 db에서 데이터를 가져와서 새로 등록하려는 이름이랑 비교해야 하는데 가져오는 걸 못하겠다 ㅠ 
            if users.filter(name = data['name']).exist():
                return JsonResponse({'message': 'name already registered'}, status=400)

            elif users.filter(user_name = data['user_name']).exist():
                return JsonResponse({'message':'username already in use'}, status=400)

            elif users.filter(email = data['email']).exist():
                return JsonResponse({'message':'email address already registered'}, status=400)

            elif users.filter(phone_number = data['phone_number']).exist():
                return JsonResponse({'message':'phone number already registered'}, status=400)
"""
