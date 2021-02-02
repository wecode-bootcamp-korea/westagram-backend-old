from django.shortcuts import render

import json
from django.views   import View
from django.http    import HttpResponse, JsonResponse

from .models        import User

class UserView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_data = data['user']

            if user_data['email_adress'] and user_data['password']:
                
                if '@' or '.' not in user_data['email_adress']:
                    return JsonResponse({'message':'@ OR . IS MISSING IN E-MAIL ADRESS'})

                if len(user_data['password']) < 8:
                    return JsonResponse({'message': 'PASSWORD HAS TO BE AT LEAST 8-DIGIT'})
                    
                user = User.objects.create(
                                            phone_number    =   user_data['phone_number'],
                                            email_adress    =   user_data['email_adress'],
                                            name            =   user_data['name'],
                                            nickname        =   user_data['nickname'],
                                            password        =   user_data['password']
                                            )
                
                return JsonResponse({'message':'SUCESS'}, status = 200)
            
            else:
                return JsonResponse({'message':'PASSWORD OR E-MAIL IS MISSING'}, status = 401)
        
        except:
            return JsonResponse({'message': 'INVALID_KEYS'}, status = 400)

