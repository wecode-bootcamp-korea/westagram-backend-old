import json

from django.views import View
from django.http  import JsonResponse

from .models      import Users


class SignUpView(View):
    def post(self, request):
        data                    = json.loads(request.body)
        MINIMUM_PASSWORD        = 8
        query_data              = Users.objects
        #query_data              = Users.objects.values('name', 'email', 'phon_number')
        
     
        if ('email' not in data.keys() or
            'name' not in data.keys() or
            'password' not in data.keys() or
            'phon_number' not in data.keys()):
            
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        
        if (query_data.filter(email= data['email']) or 
            query_data.filter(name= data['name'] ) or
            query_data.filter(phon_number= data['phon_number'])):

            return JsonResponse({'message':'Somethin is duplicated'}, status=400)
        
        
        if len(data['password']) < MINIMUM_PASSWORD:
            return JsonResponse({'message':'Password too short'}, status=400)
        
        if '@' not in data['email'] or '.' not in data['email']:
            return JsonResponse({'message':'Not included @ or . '}, status=400)
      
        else:
            Users(
            name            = data['name'],
            email           = data['email'],
			password        = data['password'],
            phon_number     = data['phon_number']
            ).save()
            
            return JsonResponse({'message':'SUCCESS'}, status=200)
    
    def get(self, request):
        user_data = Users.objects.values()

        return JsonResponse({'users':list(user_data)}, status=200)

class LogInView(View):
    def post(self, request):
        data                    = json.loads(request.body)
        query_data              = Users.objects
        
        #계정 or password 키가 안 넘어 왔을 때 error
        if 'email' not in data.keys() or 'password' not in data.keys():
            return JsonResponse({'message':'KET_ERROR'}, status=400)
        #계정 확인
    
        if not query_data.filter(email= data['email']) :
            return JsonResponse({'message':'INVALID_USER(no account)'}, status=401)
        else:        
            #로그인 성공
            confirm_data = query_data.get(email= data['email'])

            if (confirm_data.password == data['password'] and
                confirm_data.phon_number == data['phon_number']):

                return JsonResponse({'message':'SUCCESS'}, status=200)
            else: #로그인 실패(비밀번호 또는 전화번호 잘 못 입력)
                return JsonResponse({'message':'INVALID_USER'}, status=401)
    
		
 # http -v '본인 레플릿 페이지 주소' name='테스트용이름' email='테스트용이메일' password='비밀번호'

        

