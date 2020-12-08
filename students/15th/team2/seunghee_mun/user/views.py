import json
import re
import bcrypt
import jwt
from django.http     import JsonResponse
from django.views    import View
from django.core.exceptions import ValidationError
from user.models import User
from my_settings import SECRET_KEY, ALGORITHM


class UserView(View):
    def post(self, request):
            data = json.loads(request.body)
            try:
                user_email = re.match('^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{3})$', data['name'])
                user_HP    = re.match('^[0-9]{3}-[0-9]{4}-[0-9]{4}$', data['name'])
                user_id    = re.match('^[a-z0-9_-]{2,10}$', data['name'])
                password   = re.match('^\w{8, 15}$', data['password'])
                input_name = data['name']
            except:
                return JsonResponse({"message": "KEY_ERROR"}, status=400)
            
            #Key validtion
            if not user_email and not user_HP and not user_id:
                return JsonResponse({"message": "KEY_ERROR"}, status=400)	
	
            # email validtion
            if data['name'] == user_email:
                return JsonResponse({'MESSAGE' : 'EMAIL_ERROR'}, status=400)

	
	    # name validtion\
            if  data['name'] == user_id:
                return JsonResponse({'MESSAGE' : 'NAME_ERROR'}, status=400)	
		
	    # HP validion
            if  data['name'] == user_HP:
                return JsonResponse({'MESSAGE' : 'HP_ERROR'}, status=400)
		
	    # password validtion
            if  len(data['password']) < 8:
                return JsonResponse({'MESSAGE' : 'PW_ERROR'}, status=400)

            # hashed_pw
            hashed_pw = bcrypt.hashpw ( data['password'].encode('utf-8'), bcrypt.gensalt())

	    # info_overlap
            if not User.objects.filter(user_name=data['name']):
                User.objects.create(user_name=data['name'], password=hashed_pw.decode('utf-8'))
                return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)
            return JsonResponse({'MESSAGE' : 'INFO_OVERLAP_ERROR'}, status=400)


    def get(self, request):
        get_data = json.loads(request.body)

        # Key_error
        try:
            get_user_name = get_data['name']
            get_password  = get_data['password']	
        except:
            return JsonResponse ({'message': 'KEY_ERROR'}, status=400)

        User_get = User.objects.get(user_name=get_data['name'])
 

        SECRET_KEY, ALGORITHM
        # check_pw validation
        User_pw = User_get.password
        hash_pw_get = User_pw.encode('utf-8')
        if bcrypt.checkpw (get_data['password'].encode('utf-8'), hash_pw_get):
            # token create
            token = jwt.encode({'user-id' : User_get.id}, SECRET_KEY, ALGORITHM)
            token_str = token.decode('utf-8')
            return JsonResponse({'TOKEN' : token_str}, status=201)
        return JsonResponse({'MESSAGE' : 'PW_ERROR'}, status=400)

        # Invalid_user

        if not User.objects.filter(user_name=get_data['name']) or not User.objects.filter(password=get_data['password']):
            return JsonResponse({"message": "INVALID_USER"}, status=401)
        return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)	 

		
			
