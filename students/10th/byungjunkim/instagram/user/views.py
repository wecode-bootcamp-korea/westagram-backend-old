import json
from django.views import View
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from .models import User

""" 회원가입
    1. 중복되는 이름 or 이메일 early return  {'message':'ALREADY'},status=400
    2. 필수 요소가 안들어가 있으면 KeyError {'message':'INVALID_KEYS'},status=400
    3. 성공할 경우 {'message':'SUCCESS'},status=200
"""
class SignUpView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(name=data["name"]).exists() or User.objects.filter(email=data["email"]).exists():       
                return JsonResponse({'message':'ALREADY'},status=400)
            User(
                name        = data['name'],
                email       = data['email'],
                password    = data['password']
            ).save()
            return JsonResponse({'message':'SUCCESS'},status=200)
        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'},status=400)
    
    #유저리스트 보여주기
    def get(self,request):
        user=User.objects.values()
        return JsonResponse({'user':list(user)},status=200)

"""로그인
    1. 중복되는 아이디로 회원가입 되어있으면 MultipleObjectsReturned {'message':'MultiReturn'},status=401
    2. 존재하지 않는 아이디로 로그인하면 ObjectDoesNotExist {'message':'INVALID_USER'},status=401
    3. 이름을 쓰지않으면 KeyError {'message':'VACANT'},status=401
    4. 비밀번호가 맞지않으면 {'message':'WRONG_PASSWORD'},status=401
"""
class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:   
            if User.objects.get(name=data["name"]).password==data["password"]:
                return JsonResponse({'message':'SUCCESS'},status=200)
            elif  User.objects.get(name=data["name"]).password!=data["password"]:
                return JsonResponse({'message':'WRONG_PASSWORD'},status=401)
        except KeyError:
            return JsonResponse({'message':'VACANT'},status=401)
        except ObjectDoesNotExist:
            return JsonResponse({'message':'INVALID_USER'},status=401)
        except MultipleObjectsReturned :
             return JsonResponse({'message':'MultiReturn'},status=401) 
            