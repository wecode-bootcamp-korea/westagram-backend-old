import json

from django.views import View
from django.http  import JsonResponse,HttpResponse
from user.models  import User

# Create your views here.


def IndexView(request):
    return HttpResponse("Hello, world. You're at the polls index.")



class SignUpView(View):
    def post(self,request):
         try:
            data = json.loads(request.body)
            
            if len(data['password']) < 8 :
                return JsonResponse({'MESSAGE':'비밀번호를 8자 이상으로 입력하세요'},status=400)
            
            elif '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'MESSAGE':'이메일을 확인하세요'},status=400)
            
            elif User.objects.filter(name=data['name']).exists():
                return JsonResponse({'MESSAGE':'이미 가입된 이름 정보입니다'},status=400)
            
            elif User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE':'이미 가입된 이메일 정보입니다'},status=400)
            
            elif User.objects.filter(phone=data['phone']).exists():
                return JsonResponse({'MESSAGE':'이미 가입된 전화번호  정보입니다'},status=400)
            
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

           
           
class SignInView(View):
    def post(self,request):
        #return JsonResponse({'MESSAGE':data},status=400)
        try:
            data = json.loads(request.body)
            
            if not data['name'] and not data['email'] and not data['phone']:
                return JsonResponse({'MESSAGE':'계정을 입력하세요'},status=400)
                #return JsonResponse({'MESSAGE':'KEYERROR'},status=400)
            
            elif not data['password']:
                return JsonResponse({'MESSAGE':'비밀번호를 입력하세요'},status=400)
                #return JsonResponse({'MESSAGE':'KEYERROR'},status=400)
            
            elif User.objects.filter(name=data['name']).exists():
                user = User.objects.get(name=data['name'])
                
                if user.password == data['password']:
                    return JsonResponse({'MESSAGE':'SUCCESS'},status=200)
                else:
                    return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
                
            
            elif User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])
                
                if user.password == data['password']:
                    return JsonResponse({'MESSAGE':'SUCCESS'},status=200)
                else:
                    return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
                
            elif User.objects.filter(phone=data['phone']).exists():
                user = User.objects.get(phone=data['phone'])
                
                if user.password == data['password']:
                    return JsonResponse({'MESSAGE':'SUCCESS'},status=200)
                else:
                    return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

           # elif not User.objects.filter(name=data['name']).exists() and not User.objects.filter(email=data['email']).exists():
            #    return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
            else:
                return JsonResponse({'MESSAGE': 'INVALID_USER(예외)'}, status=401)

        except:
            return JsonResponse({'MESSAGE':'KEYERROR'},status=400)




     

