import json, traceback, bcrypt, jwt

from django                 import forms
from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from .models                import User
from .my_settings           import Sk

secret = Sk.SECRET_KEY
class Signup(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            signup_db = User.objects.all()            
            hashed_pw = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())      
            user = User(
                email        = data['email'],
			    password     = hashed_pw.decode('utf-8'),
            )
            user.full_clean()
            if signup_db.filter(email = data['email']).exists():
                return JsonResponse({'message':'email : already exists'}, status=400)
            user.save()
            return JsonResponse({'message':'SUCCESS'}, status=200) 
        except KeyError :
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except ValidationError as v :
            trace_back = traceback.format_exc()
            return JsonResponse({'message':'Invalid'}, status=400)  
        except json.JSONDecodeError : 
            return JsonResponse({'message':'Invalid Jason form'}, status=400) 

    def get(self, request):
            user_data = User.objects.values()
            return JsonResponse({'This is Newbie\'s data':list(user_data)}, status=200)

class Login(View):
    def post(self, request):
        data = json.loads(request.body)
        try : 
            user = User(
                email        = data['email'],
			    password     = data['password']
            )
            if bcrypt.checkpw(data['password'].encode('utf-8'), User.objects.get(email=data['email']).password.encode('utf-8')):
                access_token = jwt.encode({'email': User.objects.get(email=data['email']).email}, secret , algorithm = 'HS256') 
                return JsonResponse({'token': access_token.decode('utf-8') }, status=200)    
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        except KeyError :
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
    
    def get(self, request):
        user_data = User.objects.values()
        return JsonResponse({'Login_log':list(user_data)}, status=200)



  # if User.objects.filter(account = data['account'], password = data['password']).exists() :