# from westagram.settings import AUTH_PASSWORD_VALIDATORS
# from django.core.exceptions import ViewDoesNotExist
import json,bcrypt,jwt
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
            name    = data['name']
            email   = data['email']
            phone   = data['phone']
            password= data['password']

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_password= hashed_password.decode('utf-8')

            if '.' not in email or '@' not in email:
                return JsonResponse({'message':'error_email_form'}, status = 401)            

            if len(password)<8: 
                return JsonResponse({'message':'error_password_form'}, status = 401)            

            if User.objects.filter(name=name).exists():
                return JsonResponse({'message':'error_email_exist'}, status = 401)     

            elif User.objects.filter(email=email).exists():
                return JsonResponse({'message':'name_exist'}, status = 401)   
           
            elif User.objects.filter(phone=phone).exists():
                return JsonResponse({'message':'phone_exist'}, status = 401)            
            
            else: 
                User.objects.create(email=email, name=name, phone=phone, password=decoded_password)
                return JsonResponse({'message':'success_signup'}, status = 201)
    
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)            
        
        except JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=400)        
        

class SignInView(View):
    def post(self, request):
        try:    
            data    = json.loads(request.body)
            id      = data['id']
            password= data['password']
            
            id_set    =  User.objects.filter(Q(name=id) | Q(email=id) | Q(phone=id))
            name_set  =  User.objects.filter(name=id)
            email_set =  User.objects.filter(email=id)
            phone_set =  User.objects.filter(phone=id)

            # encoded_password = password.encode('utf-8')
            # decoded_password = User.objects.get(email=email).password

            if not id_set.exists():
                return JsonResponse({'message':'error_id_matching'}, status = 401)

            else:
                if name_set.exists():
                    for name in name_set.iterator():
                        decoded_password = User.objects.get(name=id).password
                        encoded_password = password.encode('utf-8')

                        if bcrypt.checkpw(encoded_password, decoded_password.encode('utf-8')):
                            token = jwt.encode({'name': id}, SECRET_KEY, ALGORITHM)
                            return JsonResponse({'message':'success_signin', 'access_token':token}, status = 201)
                        else:
                             return JsonResponse({'message':'error_password_matching'}, status = 401)

                elif email_set.exists():
                    for email in email_set.iterator():
                        decoded_password = User.objects.get(email=id).password
                        encoded_password = password.encode('utf-8')

                        if bcrypt.checkpw(encoded_password, decoded_password.encode('utf-8')):
                            token = jwt.encode({'email': id}, SECRET_KEY, ALGORITHM)
                            return JsonResponse({'message':'success_signin', 'access_token':token}, status = 201)
                        else:
                             return JsonResponse({'message':'error_password_matching'}, status = 401)

                elif phone_set.exists():
                    for phone in phone_set.iterator():
                        decoded_password = User.objects.get(phone=id).password
                        encoded_password = password.encode('utf-8')

                        if bcrypt.checkpw(encoded_password, decoded_password.encode('utf-8')):
                            token = jwt.encode({'phone': id}, SECRET_KEY, ALGORITHM)
                            return JsonResponse({'message':'success_signin', 'access_token':token}, status = 201)
                        else:
                             return JsonResponse({'message':'error_password_matching'}, status = 401)




            # if not User.objects.filter(id=email).exists():
            #     return JsonResponse({'message':'error_email_matching'}, status = 401)   
            
            # if User.objects.filter(email=email).exists():
            #     if bcrypt.checkpw(encoded_password, decoded_password.encode('utf-8')):

            #         token = jwt.encode({'id':email}, SECRET_KEY, ALGORITHM)
            #         print(token,"====================================")
            #         # pay=jwt.decode(token, SECRET_KEY, ALGORITHM)
            #         # print(pay,'===========================')
            #         return JsonResponse({'message':'success_signin', 'access_token':token}, status = 201)

            #     return JsonResponse({'message':'error_password_matching'}, status = 401)

        except User.DoesNotExist:
            return JsonResponse({'message': 'KEY_ERROR'}, status=401)            

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)            

        except JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=400)            



