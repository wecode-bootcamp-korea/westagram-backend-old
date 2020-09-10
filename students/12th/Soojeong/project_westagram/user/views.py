import json
from django.http    import JsonResponse
from django.views   import View
from .models        import Users
import bcrypt
import jwt
from project_westagram.settings import SECRET_KEY, ALGORITHM

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        if ('email' or 'phone_number') not in data.keys()\
            or 'user_name' not in data.keys()\
            or 'name'  not in data.keys()\
            or 'password' not in data.keys():
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        elif ("@" and ".") not in data['email']:
            return JsonResponse({'message':'INCORRECT_EMAIL_ADDRESS'}, status=400)
        
        elif len(data['password']) < 8:
           return JsonResponse({'message':'PASSWORD_TOO_SHORT'}, status=400) 

        Users(
    	    name    		= data['name'],
        	email           = data['email'],
        	phone_number    = data['phone_number'],
        	password        = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        	user_name       = data['user_name'],
        ).save()
        
        # 전번과 이메일을 null=True 로 했는데도 이메일이나 폰 넘버 중 하나만 쓰면 저장을 못함
        return JsonResponse({'message':'SUCCESS'}, status=200)
        
class LogInView(View):
    def get(self, request):           
        data = json.loads(request.body)

        # 계정정보 미입력    
        if (
            'phone_number' not in data.keys()\
            and 'email' not in data.keys()\
            and 'user_name' not in data.keys()
            ):                         
            return JsonResponse({'message':'USER_KEY_ERROR'}, status=400)

        #비밀번호 미입력
        if 'password' not in data.keys():
            return JsonResponse({'message':'KEY_ERROR'}, status=400)       

        # 입력한 계정정보(phone_number or email or user_name) 미등록
        if (
            ('phone_number' in data.keys()\
            and {'phone_number': data['phone_number']} not in list(Users.objects.values('phone_number')))\
            or ('email' in data.keys()\
            and {'email': data['email']} not in list(Users.objects.values('email')))\
            or ('user_name' in data.keys()\
            and {'user_name': data['user_name']} not in list(Users.objects.values('user_name')))\
            ):
            return JsonResponse({'message':'이메일/폰번/유저네임 등록안됨'}, status=401)
        
        # 입력한 이메일과 비밀번호 일치하면 성공 - 토큰발행
        if {'email':data['email']} in list(Users.objects.values('email')): 
            user_info       = Users.objects.get(email=data['email'])
            input_password  = data['password'].encode('utf-8')
            db_password     = user_info.password.encode('utf-8')

            if bcrypt.checkpw(input_password, db_password):
                access_token    = jwt.encode(   {'user_id': user_info.id}, SECRET_KEY, ALGORITHM )
                token_decoded   = jwt.decode(   access_token, SECRET_KEY, ALGORITHM  )
                return JsonResponse({'Authorized': access_token.decode('utf-8')}, status=200)

        return JsonResponse({'message':'PASSWORD_NOT_MATCHING'}, status=401)

        #우선 이메일로만 로그인 가능.
        """
        elif {'phone_number':data['phone_number']} in list(Users.objects.values('phone_number')): 
            user_info       = Users.objects.get(phone_number=data['phone_number'])
            input_password  = data['password'].encode('utf-8')
            db_password     = user_info.password.encode('utf-8') 
            if not bcrypt.checkpw(input_password, db_password): 
                return JsonResponse({'message':'KINVALID_USER'}, status=401) 

        elif {'user_name':data['user_name']} in list(Users.objects.values('user_name')): 
            user_info       = Users.objects.get(user_name=data['user_name'])
            input_password  = data['password'].encode('utf-8')
            db_password     = user_info.password.encode('utf-8') 
            if not bcrypt.checkpw(input_password, db_password): 
                return JsonResponse({'message':'KINVALID_USER'}, status=401) 
        """
         
