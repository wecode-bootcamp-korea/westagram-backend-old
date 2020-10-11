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
        try :
            data = json.loads(request.body)
            if len(data['password']) < 8 :
                return JsonResponse({'MESSAGE':'비밀번호를 8자 이상으로 입력하세요'},status=400)
            elif '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'MESSAGE':'이메일을 확인하하세요'},status=400)
            elif User.objects.filter(name=data['name']).exists():
                return JsonResponse({'MESSAGE':'이미 가입된 정보입니다'},status=400)
            else:
                User(
                    name = data['name'],
                    phone = data['phone'],
                    email = data['email'],
                    password = data['password']
                    ).save()
                return JsonResponse({'MESSAGE':'SUCCESS'},status=200)

        except:
            return JsonResponse({'MESSAGE':'KEYERROR'},status=400)




     

