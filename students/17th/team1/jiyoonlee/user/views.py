import json

from django.http import JsonResponse
from django.views import View

from .models import User


class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            mobile_number = data['mobile_number']
            email         = data['email']
            full_name     = data['full_name']
            username      = data['username']
            password      = data['password']

            if mobile_number is None and email is None:
                return JsonResponse(
                    {'message': '휴대폰 번호나 이메일을 입력하세요.'}, 
                    status=400
                )

            if email is not None:
                if '@' not in email or '.' not in email:
                    return JsonResponse(
                        {'message': '이메일 형식을 확인하세요.'}, 
                        status=400
                    )
            
            if len(password) < 8:
                return JsonResponse(
                    {'message': '최소 8자 이상으로 구성된 비밀번호를 생성해주세요.'},
                    status=400
                )
            
            if mobile_number is not None and User.objects.filter(mobile_number=data['mobile_number']).exists():
                return JsonResponse(
                    {'message': '이미 등록된 번호입니다.'},
                    status=400
                )

            if email is not None and User.objects.filter(email=data['email']).exists():
                return JsonResponse(
                    {'message': '이미 등록된 이메일입니다.'},
                    status=400
                )

            if User.objects.filter(username=data['username']).exists():
                return JsonResponse(
                    {'message': '이미 사용중인 username입니다.'},
                    status=400
                )


            User.objects.create(
                mobile_number = data['mobile_number'],
                email = data['email'],
                password = data['password'],
                full_name= data['full_name'],
                username= data['username']
            )


            return JsonResponse(
                {'message': '회원가입에 성공하였습니다'},
                status=200
            )


        except KeyError:
            return JsonResponse(
                {'message': 'KEY_ERROR'},
                status=400
            )
