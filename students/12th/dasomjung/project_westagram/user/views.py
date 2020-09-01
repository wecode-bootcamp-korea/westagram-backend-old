import json
import re
from django.views import View
from django.http import JsonResponse
from .models import Users


class SignUp(View):
    def post(self, request):
        data = json.loads(request.body)


'''
        # 회원가입시 이메일을 사용할 경우 전달이 안된경우
        try:

        except:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        # 회원가입시 이메일을 사용할 경우 @ 과 . 이 포함 안된경우 에러 반환
        try:
            email = Users.email.get(pk=request.POST[@.])
        except:
            return JsonResponse({'message': ''}, status=)

        # 아이디(전화번호, 사용자이름, 이메일)가 중복된 경우 에러 반환

        # 비밀번호 전달이 안된 경우
        try:

        except:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        # 비밀번호가 8자리 미만일 경우 에러 반환
        try:
            password = Users.password.get(pk=request.POST[\d{8, }])
        except:
            return JsonResponse({'message': ''}, status=)
'''
        Users(
            name=data['name'],
            user_name=data['user_name']
            number=data['number'],
            email=data['email'],
            password=data['password']
        ).save()

        return JsonResponse({'message': 'SUCCESS'}, status=200)

    def get(self, request):
        user_data = Users.objects.values()
        return JsonResponse({'users': list(user_data)}, status=200)
