import json
from django.views  import View
from django.http   import JsonResponse
from .models       import Account
import re

class SignUp(View): 
    def post(self, request): 
        data = json.loads(request.body)
         
        try:

            if re.search("@",data['email']) == None or re.search("\.",data['email']) == None:
                return JsonResponse({"message": "email required"}, status=400)

            if len(data['password']) < 8: 
                return JsonResponse({"message": "password number must longer than 8"}, status=400)

   
            if Account.objects.filter(name=data['name']):
                return JsonResponse({"message": "already exist name"}, status=400)
 
            if Account.objects.filter(phone_num=data['phone_num']):
                return JsonResponse({"message": "already exist phone number"}, status=400)

            if Account.objects.filter(email=data['email']):
                return JsonResponse({"message": "already exist phone number"}, status=400)


            Account(
                name      = data['name'],
                email     = data['email'],
                password  = data['password'],
                phone_num = data['phone_num']

            ).save()
            return JsonResponse({"message": 'Success'},   status=200)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

