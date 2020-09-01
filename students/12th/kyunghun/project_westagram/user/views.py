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
		
 # http -v '본인 레플릿 페이지 주소' name='테스트용이름' email='테스트용이메일' password='비밀번호'

        

