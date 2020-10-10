import json

from django.views import View
from django.http  import JsonResponse
from user.models  import User
from django.http  import HttpResponse

# Create your views here.


def IndexView(request):
    return HttpResponse("Hello, world. You're at the polls index.")



class SignUpView(View):
    def post(self,request):
        data     = json.loads(request.body)
        '''name     = User.objects.create(name=data['name'])
        email    = User.objects.create(email=data['email'])
        password = User.objects.create(password=data['password'])'''
        name = data['name'],
        email = data['email'],
        password = data['password']
        '''        
        if not name:
            return JsonResponse({'MESSAGE':'KEY_ERROR'},status=400)
        
        else:
            if len(password) < 8 :
                return JsonResponse({'MESSAGE':'비밀번호를 8자 이상 입력해주세요'},status=400)
            elif User.objects.filter(name=name).exists() == True :
                return JsonResponse({"message" : "이미 존재하는 아이디입니다."}, status = 401)
            elif User.objects.filter(email=email).exists() == True :
                return JsonResponse({"message" : "이미 존재하는 아이디입니다."}, status = 401)
'''

