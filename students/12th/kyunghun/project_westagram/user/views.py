import json
import jwt
import bcrypt

from datetime           import datetime, timedelta
from django.views       import View
from django.http        import JsonResponse
from django.utils       import timezone

from .models            import User
from westagram.settings import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        data                    = json.loads(request.body)
        MINIMUM_PASSWORD        = 8
        query_data              = User.objects
        
        if ('email' not in data.keys() or
            'name' not in data.keys() or
            'password' not in data.keys() or
            'phon_number' not in data.keys()):
            return JsonResponse({'message':'KEY_ERROR'}, status= 400)
        
        if (query_data.filter(email= data['email'])  or 
            query_data.filter(name= data['name'] ) or
            query_data.filter(phon_number= data['phon_number'])):
            return JsonResponse({'message':'Something is duplicated'}, status= 400)
        
        if len(data['password']) < MINIMUM_PASSWORD:
            return JsonResponse({'message':'Password too short'}, status= 400)
        
        if '@' not in data['email'] or '.' not in data['email']:
            return JsonResponse({'message':'Not included @ or . '}, status= 400)
        else:
            password            = data['password']
            password_hashed     = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            User(
            name                = data['name'],
            email               = data['email'],
			password            = password_hashed.decode('utf-8'),
            phon_number         = data['phon_number']
            ).save()
            return JsonResponse({'message':'SUCCESS'}, status= 200)
    
    def get(self, request):
        user_data = User.objects.values()
        return JsonResponse({'users':list(user_data)}, status= 200)

class LogInView(View):
    def post(self, request):
        data                    = json.loads(request.body)
        EXP_TIME_HOURS          = 1
        
        if 'email' not in data.keys() or 'password' not in data.keys():
            return JsonResponse({'message':'KET_ERROR'}, status= 400)
    
        if not User.objects.filter(email= data['email']) :
            return JsonResponse({'message':'INVALID_USER(no account)'}, status= 401)
        else:
            user_data           = User.objects.get(email= data['email'])        
            confirm_data        = user_data.password
            input_password      = data['password']
            check_password      = bcrypt.checkpw(input_password.encode('utf-8'),\
                                            confirm_data.encode('utf-8'))
            if check_password:
                exp             = timezone.now() + timedelta(hours= EXP_TIME_HOURS)
                encoded_jwt     = jwt.encode({
                'user_id' : user_data.id,
                'exp'     : exp
                }, SECRET_KEY, algorithm= ALGORITHM)
                token           = encoded_jwt.decode('utf-8')
                return JsonResponse({'Authorization': token}, status=200)
            else: 
                return JsonResponse({'message':'INVALID_USER'}, status= 401)
    

        

