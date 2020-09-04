import json
import re
from django.views import View
from django.http  import JsonResponse
from .models      import Users


class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if Users.objects.filter(email=data['email']).exists():   # 아이디(email) 존재할 때
                return JsonResponse({'message': 'Already Exist'}, status = 400)
            
            if len(data['password']) < 8:
                return JsonResponse({'message': 'Too short'}, status=400)   # 에러 반환

            Users.objects.create(
                email    = data['email'],
                password = data['password']
            ).save()

            return JsonResponse({'message': 'SUCCESS'}, status=200)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)   # 아이디(eamil)이나 비밀번호 키가 잘못되었을 때
        
   
        # 회원가입시 이메일을 사용할 경우 @ 과 . 이 포함 안된경우 에러 반환
        # if Users.email.filter(r'[^@.]$') == True:     
        # if not (Users.objects.get(email__contains='@') or Users.objects.get(email__contains='.')) == True:
        # shell 에서는 정상 작동 하는데 여기서는 안되네요.. 이미 저장된 정보만 가지고 할 수 있는 메소드 일까요?ㅠㅠ
            # return JsonResponse({'message': 'Incorrect format'}, status=400)    # 에러 반환 

    def get(self, request):
        user_data = Users.objects.values()
        return JsonResponse({'users': list(user_data)}, status=200)


class SignIn(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if not Users.objects.filter(email=data['email']).exists():   # 아이디(email) 존재하지 않을때
                return JsonResponse({'message':'INVALID_USER'}, status=401)

            if not Users.objects.filter(password=data['password']):    # 비밀번호 틀렸을 때
                return JsonResponse({'message':'INVALID_USER'}, status=401)

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)   # 아이디, 비번 계정 전달되지 않았을 때