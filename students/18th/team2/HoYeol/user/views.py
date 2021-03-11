import json,bcrypt,jwt
from json.decoder     import JSONDecodeError

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

            if '.' not in email or '@' not in email:
                return JsonResponse({'message':'error_email_form'}, status=401)            

            if len(password)<8: 
                return JsonResponse({'message':'error_password_form'}, status=401)            

            if User.objects.filter(Q(name=name) | Q(email=email) | Q(phone=phone)).exists:
                return JsonResponse({'message':'id_exist'}, status = 401)           
               
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_password= hashed_password.decode('utf-8')
            
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
            user  = User.objects.get(Q(name=id) | Q(email=id) | Q(phone=id))

            if user is not id:
                return JsonResponse({'message':'error_id_matching'}, status=401)

            if user is id:
                decoded_password = user.password
                encoded_password = password.encode('utf-8')
                bcrypt.checkpw(encoded_password, decoded_password.encode('utf-8'))
                token = jwt.encode({'user':user.id}, SECRET_KEY, ALGORITHM)
                return JsonResponse({'message':'success_signin', 'access_token':token}, status=201)
            
            return JsonResponse({'message':'error_password_matching'}, status = 401)

        except User.MultipleObjectsReturned:
            return JsonResponse({'message': 'KEY_ERROR'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message': 'KEY_ERROR'}, status=401)            

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)            

        except JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=400)            



