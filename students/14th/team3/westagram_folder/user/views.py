import json
from django.views import View
from django.http  import JsonResponse
from .models  import Account
# 치킨먹고싶다...
class SignUpView(View):
    def post(self, request): #포스트로 받을 시 저장
        data = json.loads(request.body)
        signupdb = Account.objects.all() #유저 테이블정보 다 가져와
        try:        
            user = Account(
                name         = data['name'],
                phone_number = data['phone_number'],
                email        = data['email'],
                password     = data['password'])
            if "@" not in data['email'] or "." not in data['email']:
                return JsonResponse({"message" : "email_error"}, status = 400)
            elif len(data['password']) < 8 :
                return JsonResponse({"message" : "short_password"}, status = 400)
            elif Account.objects.filter(email = data['email']).exists() or Account.objects.filter(name = data['name']).exists() or Account.objects.filter(phone_number = data['phone_number']).exists() :
                return JsonResponse({"message" : "duplicated_information"}, status = 401)
            else:
                Account.objects.create(
                    name         = data['name'],
                    phone_number = data['phone_number'],
                    email        = data['email'],
                    password     = data['password'])
                return JsonResponse({"message" : "SUCCESS"},                status = 201)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"},                  status = 400)

    def get(self, request): #겟으로 받을시 유저테이블에 있는것 출력
        account_data = Account.objects.values()
        return JsonResponse({'Account Data' : list(account_data)}, status = 200)

class LoginView(View):
    def post(self, request):
        data        = json.loads(request.body)
        user_password = data['password']

        try:
            if 'name' not in data and 'email' not in data and 'phone_number' not in data:
                return JsonResponse({'message' : 'KEY_ERROR'},   status = 400)
            elif 'password' not in data:
                return JsonResponse({'message' : 'KEY_ERROR'},   status = 400)
            elif Account.objects.filter(email = data['email']).exists(): #계정이 존재한다면
                exist_user = Account.objects.get(email = data['email'])
                if exist_user.password == data['password']: #존재계정의 패스워드와 입력된 패스워드가 같다면
                    return JsonResponse({"message" : "SUCCESS"}, status = 200)
                return JsonResponse({"message" : "INVALID_USER"}, status = 401)
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'},  status = 400)

    def get(self, request): #get메쏘드로 회원가입된 데이터들을 list형태로 반환
        account_data = Account.objects.values()
        return JsonResponse({'Login' : list(account_data)}, status = 200)
        
