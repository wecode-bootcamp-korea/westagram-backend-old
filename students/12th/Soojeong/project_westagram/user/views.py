import json
from django.http    import JsonResponse
from django.views   import View
from .models        import Users

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
                  
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
        
        return JsonResponse({'message':'SUCCESS'}, status=200)
        # null=True 로 했는데도 이메일이나 폰 넘버 중 하나만 쓰면 저장을 못함 남..! ㅠㅠ


class LogInView(View):
    def get(self, request):           
        data = json.loads(request.body)
        print(data)

        # 계정정보 미입력    
        #if ('phone_number' not in data.keys()) and ('email' not in data.keys()) and ('user_name' not in data.keys()):
        #    return JsonResponse({'message':'아이디 입력하세요'}, status=400)
        
        if (
            ('phone_number' and 
            'email' and
            'user_name')
            not in data.keys()
            ):
            return JsonResponse({'message':'아이디 입력하세요'}, status=400)


        #비밀번호 미입력
        if 'password' not in data.keys():
            return JsonResponse({'message':'비번입력 안함'}, status=400)       

        # 입력한 로그인수단이 존재하지 않는 경우 (우선 무조건 이메일로만 가입한다고 가정)
        if {'email':data['email']} not in list(Users.objects.values('email')):
            return JsonResponse({'message':'이메일 주소 없음'}, status=401)

        # 이메일이 있는 경우, 비번이 틀리면 
        if {'email':data['email']} in list(Users.objects.values('email')): # 입력한 이메일이 데이터에 있다면
            user_info = Users.objects.filter(email=data['email']) # 해당 객체를 받아와서
            if user_info.values('password')[0]['password'] != data['password']: # 입력한 비번과 객체의 비번이 맞나 확인
                return JsonResponse({'message':'KEY ERROR'}, status=401) 
        
        return JsonResponse({'message':'SUCCESS'}, status=200) 
