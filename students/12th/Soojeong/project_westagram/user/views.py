import json
from django.http    import JsonResponse
from django.views   import View
from .models        import Users

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        print(list(Users.objects.all()))

        if ('email' or 'phone_number') not in data.keys()\
            or 'user_name' not in data.keys()\
            or 'name'  not in data.keys()\
            or 'password' not in data.keys():
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        elif ("@" and ".") not in data['email']:
            return JsonResponse({'message':'email address incorrect'}, status=400)
        
        elif len(data['password']) < 8:
           return JsonResponse({'message':'password must be longer than 8 characters'}, status=400)
                
        Users(
    	    name    		= data['name'],
        	email           = data['email'],
        	phone_number    = data['phone_number'],
        	password        = data['password'],
        	user_name       = data['user_name'],
        ).save()
        
        # 전번과 이메일을 null=True 로 했는데도 이메일이나 폰 넘버 중 하나만 쓰면 저장을 못함..!
        return JsonResponse({'message':'SUCCESS'}, status=200)
        


class LogInView(View):
    def get(self, request):           
        data = json.loads(request.body)

        # 계정정보 미입력    
        if (
            ('phone_number' and 
            'email' and
            'user_name')
            not in data.keys()
            ):
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


        #비밀번호 미입력
        if 'password' not in data.keys():
            return JsonResponse({'message':'KEY_ERROR'}, status=400)       

        # 입력한 로그인수단이 존재하지 않는 경우 (우선 무조건 이메일로만 가입한다고 가정)
        if {'email':data['email']} not in list(Users.objects.values('email')):
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        # 이메일이 있는 경우, 비번이 틀림
        if {'email':data['email']} in list(Users.objects.values('email')): 
            user_info = Users.objects.filter(email=data['email']) 
            if user_info.values('password')[0]['password'] != data['password']:
                return JsonResponse({'message':'KINVALID_USER'}, status=401) 
        
        return JsonResponse({'message':'SUCCESS'}, status=200) 
