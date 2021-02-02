import json
import bcrypt
import re
import jwt

from django.http    import JsonResponse
from django.views   import View
from user.models    import User
from my_settings    import SECRET, ALGORITHM

class SignupView(View):
    def post(self, request):   
        
        try:
            data = json.loads(request.body)

            user=User(
                account     = data.get('account'),
                email       = data.get('email'),
                phone       = data.get('phone'),
                password    = data['password'],
            )

            p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
            
            if len(user.email) == 0:
                return JsonResponse({'MESSAGE':"DIDN'T INPUT EMAIL"},status = 400)
            
            if len(user.password) == 0:
                return JsonResponse({'MESSAGE':"DIDN'T INPUT PASSWORD"},status = 400)

            if user.email and p.match(user.email) == None:
                return JsonResponse({'MESSAGE':'INVAILD_EMAIL_ADDRESS'},status = 400)
            
            if user.account and User.objects.filter(account = user.account).exists():
                return JsonResponse({'MESSAGE':'EXISTING ID'}, status=400)  
            
            if user.email and User.objects.filter(email = user.email).exists():
                return  JsonResponse({'MESSAGE':'EXISTING MAIL'}, status=400)
            
            if user.phone and User.objects.filter(phone = user.phone).exists():
                return  JsonResponse({'MESSAGE':'EXISTING NUMBER'}, status=400)
            
            if len(data['password']) < 8:
                return JsonResponse({'MESSAGE':'PASSWORD TOO SHORT'}, status=400)
            
            if not '@' and '.' in data['email']:
                return JsonResponse({'MESSAGE':'INVALID EMAIL'}, status=400)
            
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

            # user=User(
            # account     = data.get('account', None),
            # email       = data.get('email', None),
            # phone     = data.get('phone', None),
            # password    = data['password'],
            #  )
            user.save()
            # User.objects.create(
            #     account = account, 
            #     email = email, 
            #     phone = phone, 
            #     password = hashed_password.decode('utf-8')
            # )    
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
    
        except KeyError :
            return JsonResponse({'MESSAGE':'KEY ERROR'}, status=400)

class LogInView(View):
    def post(self, request):

        data        = json.loads(request.body)
        signup_db   = User.objects.all()
        password    = data['password']
        try:
            if not signup_db.filter(email = data['email']).exists():
                return JsonResponse({'MESSAGE':'INVALID LOGIN ID'}, status=400)

            if signup_db.filter(email = data['email']).exists():
                login_id = User.objects.get(email = data['email'])
                if bcrypt.checkpw(password.encode('utf-8'), login_id.password.encode('utf-8')):
                    user_token = jwt.encode({'user_id': login_id.id}, SECRET, algorithm=ALGORITHM)
                    return JsonResponse({'MESSAGE':user_token}, status=200)
                else:
                    return JsonResponse({'MESSAGE':'INVALID PASSWORD'}, status= 401)
            
        except KeyError :
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

