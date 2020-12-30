import json
import re
from django.http  import JsonResponse
from django.views import View

from user.models  import User

class SignUpView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']
            MIN_LEN_PWD = 8

                    
            p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

            if not email and password: 
                return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
            
            if len(password) < MIN_LEN_PWD: 
                return JsonResponse({'MESSAGE':f'PASSWORD SHOULD BE OVER {MIN_LEN_PWD} CHAR'}, status=400)
 
            if not p.match(email):
                return JsonResponse({'MESSAGE':'EMAIL ERROR.'}, status=400)
            
            if not User.objects.filter(email=email).exists(): 
                User.objects.create(
                                    password=data['password'],
                                    email   =data['email']                               
                                    )
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
            
            return JsonResponse({'MESSAGE':'EMAIL ALREADY EXISTS.'}, status=400)
            
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'DOES NOT EXISTS'}, status=400)

        except KeyError:
            return JsonResponse({'MESSAGE':"KEY ERROR OCCUR"}, status=400)


    def get(self, request):
        result = [user_info.name for user in User.objects.all()]
        return JsonResponse({'result':result}, status=200)

