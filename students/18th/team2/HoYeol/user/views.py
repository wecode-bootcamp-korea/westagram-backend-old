# from westagram.settings import AUTH_PASSWORD_VALIDATORS
# from django.core.exceptions import ViewDoesNotExist
import json, bcrypt, jwt
from json.decoder     import JSONDecodeError
from django.db.models.expressions import Exists
from django.db.models import Q
from django.views     import View
from django.http      import JsonResponse
from .models          import User
from my_settings      import SECRET_KEY, ALGORITHM


class SignUpView(View):
    def post(self, request):
        try:
            data    = json.loads(request.body)
            # name    = data['name']
            email   = data['email']
            # phone   = data['phone']
            password= data['password']

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_password= hashed_password.decode('utf-8')

            if '.' not in email or '@' not in email:
                return JsonResponse({'message':'error_email_form'}, status = 401)            

            if len(list(password))<8:
                return JsonResponse({'message':'error_password_form'}, status = 401)            

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message':'error_email_exist'}, status = 401)     

            # if User.objects.filter(name=name).exists():
            #     return JsonResponse({'message':'name_exist'}, status = 401)   
           
            # if User.objects.filter(phone=phone).exists():
            #     return JsonResponse({'message':'phone_exist'}, status = 401)            
            
            else: 
                User.objects.create(email=email, password=decoded_password)
                return JsonResponse({'message':'success_signup'}, status = 201)
    
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)            
        
        except JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=400)        
        

class SignInView(View):
    def post(self, request):
        try:    
            data    = json.loads(request.body)
            email   = data['email']
            password= data['password']
            
            encoded_password = password.encode('utf-8')
            decoded_password = User.objects.get(email=email).password

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message':'error_email_matching'}, status = 401)   
            
            if User.objects.filter(email=email).exists():
                if bcrypt.checkpw(encoded_password, decoded_password.encode('utf-8')):

                    token = jwt.encode({'id':email}, SECRET_KEY, ALGORITHM)
                    print(token,"====================================")
                    # pay=jwt.decode(token, SECRET_KEY, ALGORITHM)
                    # print(pay,'===========================')
                    return JsonResponse({'message':'success_signin', 'access_token':token}, status = 201)

                return JsonResponse({'message':'error_password_matching'}, status = 401)

        except User.DoesNotExist:
            return JsonResponse({'message': 'KEY_ERROR'}, status=401)            

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)            

        except JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=400)            



