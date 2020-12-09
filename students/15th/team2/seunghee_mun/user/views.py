import json, re, bcrypt, jwt
from django.http     import JsonResponse
from django.views    import View
from django.core.exceptions import ValidationError
from user.models import User
from my_settings import SECRET_KEY, ALGORITHM


class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        user_email = '^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{3})$'
        user_HP = '^[0-9]{3}-[0-9]{4}-[0-9]{4}$'
        user_id = '^[a-z0-9_-]{2,10}$'
        password = '^\w{8, 15}$'

        try:
            input_name = data['name']
            input_pw = data['password']
        except:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        print('==================== Key Check ======================')
        # Key val
        print(re.match(user_email, data['name']))
        print(re.match(user_HP, data['name']))
        print(re.match(user_id, data['name']))
        print(re.match(password, data['password']))

        if not re.match(user_email, data['name']) and not re.match(user_HP, data['name']) and not re.match(user_id, data['name']):
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        print('==================== Key OK ======================')


        
        #print('==================== Email Check ======================')
        # Email val
        # 
        #if not re.match(user_email, data['name']) and not re.match(user_HP, data['name']):
        #        return JsonResponse({"message": "EMAIL_ERROR"}, status=400)
        
        #print('==================== Email OK ======================')

        
        print('==================== PW Check ======================')
        # Password val
        if len(data['password']) < 8:
                return JsonResponse({"message": "PW_ERROR"}, status=400)
        print('====================   PW OK    ======================')


        print('====================   OVERLAP Check  ======================')
        # hashed_pw
        hashed_pw = bcrypt.hashpw ( data['password'].encode('utf-8'), bcrypt.gensalt())

        # info_overlap
        if not User.objects.filter(user_name=data['name']):
            User.objects.create(user_name=data['name'], password=hashed_pw.decode('utf-8'))
            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)
        return JsonResponse({'MESSAGE' : 'INFO_OVERLAP_ERROR'}, status=400)
       
class SigninView(View):
    def post(self, request):
        get_data = json.loads(request.body)

        # Key_error
        try:
            get_user_name = get_data['name']
            get_password  = get_data['password']	
        except:
            return JsonResponse ({'message': 'KEY_ERROR'}, status=400)

        User_get = User.objects.get(user_name=get_data['name'])
 

        # check_pw validation
        User_pw     = User_get.password
        hash_pw_get = User_pw.encode('utf-8')
        if bcrypt.checkpw (get_data['password'].encode('utf-8'), hash_pw_get):
            # token create
            token     = jwt.encode({'user-id' : User_get.id}, SECRET_KEY, ALGORITHM)
            token_str = token.decode('utf-8')
            return JsonResponse({'TOKEN' : token_str}, status=201)
        return JsonResponse({'MESSAGE' : 'PW_ERROR'}, status=400)

        # Invalid_user

        if not User.objects.filter(user_name=get_data['name']) or not User.objects.filter(password=get_data['password']):
            return JsonResponse({"message": "INVALID_USER"}, status=401)
        return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)	 

		
			
