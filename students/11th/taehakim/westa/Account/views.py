import json
from django.views  import View
from django.http   import JsonResponse
from .models       import Account
import re
import bcrypt
import jwt

SECRET = 'secret'

class SignUp(View): 
    def post(self, request): 
        data = json.loads(request.body)
         
        try:


            if re.search("@",data['email']) == None or re.search("\.",data['email']) == None:
                return JsonResponse({"message": "email required"}, status=400)

            if len(data['password']) < 8: 
                return JsonResponse({"message": "password number must be longer than 8"}, status=400)

   
            # if Account.objects.filter(name=data['name']):
            #     return JsonResponse({"message": "already exist name"}, status=400)
 
            # if Account.objects.filter(phone_num=data['phone_num']):
            #     return JsonResponse({"message": "already exist phone number"}, status=400)

            if Account.objects.filter(email=data['email']):
                return JsonResponse({"message": "already exist email"}, status=400)
          
            change_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())



            Account(
                # name      = data['name'],
                name =  'testname',
                email     = data['email'],
                password  = change_password.decode('utf-8'),
                # phone_num = data['phone_num']
                phone_num='testphonenum'

            ).save()
            return JsonResponse({"message": 'Success'},   status=200)
        
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class SignIn(View):
    def post(self, request): 
        data = json.loads(request.body)
         
        try:  

            # if Account.objects.filter(name=data['name']):
            #     if bcrypt.checkpw(data["password"].encode('utf-8'), Account.objects.get(name=data['name']).password.encode('utf-8')):
            #         access_token = jwt.encode({'email' : data['email']}, SECRET, algorithm = 'HS256').decode('utf-8')
            #         return JsonResponse({"token": access_token},   status=200)

            if data['email']=="":
                return JsonResponse({"message": "please enter your email"})

            if data['password']=="":
                return JsonResponse({"message": "please enter your password"})


            if Account.objects.filter(email=data['email']):
                if bcrypt.checkpw(data["password"].encode('utf-8'), Account.objects.get(email=data['email']).password.encode('utf-8')):
                    access_token = jwt.encode({'email' : data['email']}, SECRET, algorithm = 'HS256').decode('utf-8')
                    return JsonResponse({"token": access_token},   status=200)
            
            else:
                return JsonResponse({"message": "INVALID_USER"}, status=401)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)