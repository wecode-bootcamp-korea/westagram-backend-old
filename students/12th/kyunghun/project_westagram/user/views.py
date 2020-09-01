import json

from django.views import View
from django.http  import JsonResponse

from .models      import Users


class SignUp(View):
    def post(self, request):
        data                    = json.loads(request.body)
        MINIMUM_PASSWORD        = 8
        
        query_data              = Users.objects.values('name', 'email', 'phon_number')
        
        for query_index in range(len(query_data)):
            query_list = list(query_data[query_index].values())
            for check_data in [data['name'], data['email'], data['phon_number']]:
                if check_data in query_list:
                    return JsonResponse({'message':'Somethin is duplicated'}, status=400)
        
        
        if len(data['password']) < MINIMUM_PASSWORD:
            return JsonResponse({'message':'Password too short'}, status=400)
        
        if '@' not in data['email'] or '.' not in data['email']:
            return JsonResponse({'message':'Not included @ or . '}, status=400)

        if 'email' not in data.keys():
            return JsonResponse({'message':'KET_ERROR'}, status=400)
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

class SignIn(View):
    def post(self, request):
        data                    = json.loads(request.body)
        query_data_email        = Users.objects.values('email')
        query_data              = Users.objects.values('email', 'password', 'phon_number')
        
        #계정 or password 키가 안 넘어 왔을 때 error
        if 'email' not in data.keys() or 'password' not in data.keys():
            return JsonResponse({'message':'KET_ERROR'}, status=400)
        #계정 확인
        for query_index in range(len(query_data_email)):
            query_email_list = list(query_data_email[query_index].values())
            #계정 없으면 error
            if data['email'] not in query_email_list :
                return JsonResponse({'message':'INVALID_USER(no account)'}, status=401)
            else:        
                #로그인 성공
                for query_index in range(len(query_data)):
                    query_list = list(query_data[query_index].values())
                    if query_list == [data['email'], data['password'], data['phon_number']]:
                        return JsonResponse({'message':'SUCCESS'}, status=200)
                    else: #로그인 실패(비밀번호 또는 전화번호 잘 못 입력)
                        return JsonResponse({'message':'INVALID_USER'}, status=401)
        
        
        
        
        
        
        
        
        
        
        # 메일, 비밀번호, 전화번호가 모두 맞아야 로그인, 해당 메일 계정이 있는지는 확인 안함. 
        
        # query_data              = Users.objects.values('email','password', 'phon_number')
        
        # #계정 or password 키가 안 넘어 왔을 때 error
        # if 'email' not in data.keys() or 'password' not in data.keys():
        #     return JsonResponse({'message':'KET_ERROR'}, status=400)
        # #로그인 성공
        # for query_index in range(len(query_data)):
        #     query_list = list(query_data[query_index].values())
        #     if query_list == [data['email'], data['password'], data['phon_number']]:
        #         return JsonResponse({'message':'SUCCESS'}, status=200)
        #     else:
        #         return JsonResponse({'message':'LogIn FAIL'}, status=400)
                
        
        
		
 # http -v '본인 레플릿 페이지 주소' name='테스트용이름' email='테스트용이메일' password='비밀번호'

        

