import json
import re

from django.http  import JsonResponse, HttpResponse
from django.views import View
from user.models  import Users

def is_valid(text, regex):

    return re.compile(regex).match(text) != None

class UserView(View):    

    def post(self,request):
        
        pw_regex    = '^[A-Za-z0-9@#$%^&+=]{8,}$'
        email_regex = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
     
        data = json.loads(request.body)
        
        try:
            
            assert is_valid(data['email'],email_regex), "INVALID_EMAIL_FORMAT"
            assert is_valid(data['password'],pw_regex), "INVALID_PW_FORMAT"

            if Users.objects.filter(email = data['email']): 
                return JsonResponse({"MESSAGE" : "USER_ALREADY_EXISTS"},status = 400)
                
            else:
                Users.objects.create(email = data["email"],password = data["password"])   
             
                # restapi 시점에서 201은 생성을 의미 !
                return HttpResponse(status =201)

        except KeyError:
            return JsonResponse({'message': "INVALID_KEY"},status=400)
        
        except AssertionError as e:
            return JsonResponse({"MESSAGE": f"{e} " + data['email'] + data['password']}, status = 400)



