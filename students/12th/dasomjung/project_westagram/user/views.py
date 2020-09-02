import json
import re
from django.views import View
from django.http  import JsonResponse
from .models      import Users


class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)

        # 회원가입시 휴대폰번호와 이메일 중 이메일을 사용할 경우 전달이 안되었을 때 에러 반환
        if Users.objects.filter('email') == False:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
   
        # 회원가입시 이메일을 사용할 경우 @ 과 . 이 포함 안된경우 에러 반환
        if Users.email.filter(r'[^@.]$') == True:     
        # if not (Users.objects.get(email__in='@') or Users.objects.get(email__in='.')) == True:
        # 이게 더 맞을지.....
            return JsonResponse({'message': 'Incorrect format'}, status=400)    # 에러 반환 

        # 아이디(이메일)가 중복된 경우 에러 반환
        if Users.objects.filter(['email']).exists() == True:
            return JsonResponse({'message': 'Already Exist'}, status=409)    # 에러 반환
        
        # 비밀번호 전달이 안된 경우
        if not Users.objects.filter('password') == True:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        # 비밀번호가 8자리 미만일 경우 에러 반환
        if Users.password.filter(r'\d{,7}$') == True:
        # if Users.objects.filter(password__range(8)) == True:
        # 이게 더 맞을지...
            return JsonResponse({'message': 'Too short'}, status=400)   # 에러 반환

        Users(
            email           = data['email'],
            password        = data['password']
        ).save()

        return JsonResponse({'message': 'SUCCESS'}, status=200)

    def get(self, request):
        user_data = Users.objects.values()
        return JsonResponse({'users': list(user_data)}, status=200)
