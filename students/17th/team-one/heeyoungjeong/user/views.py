import json
from django.http import JsonResponse, HttpResponse
from django.views import View

from user.models import User

class SignUp(View):
    # 기존 회원인가 아닌가 확인
    # 기존 회원이 아니면 create
    # email @ . 가 없으면 유효하지 않다고 리턴
    def post(self, request):

        data = json.loads(request.body)
        print(data)
        # request 검증 #1 : name, user_name, email, password 확인
        check_lst = ['name', 'user_name', 'email', 'password']
        for key in check_lst:
            if key not in data.keys():
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

        # request 검증 #2 : email 유효성 확인
        if not '@' in data['email'] or not '.' in data['email']:
            return JsonResponse({'message':'The email is not valid'}, status=400)

        # request 검증 #3 : password 유효성 확인
        if not 8 <= len(data['password']):
            return JsonResponse({'message': 'The password is not valid'}, status=400)

        # 기존회원 여부 확인을 위한 객체 생성
        user = User.objects.filter(email=data['email'])

        # 신규회원 생성
        if not user:
            User.objects.create(
                name      = data['name'],
                user_name = data['user_name'],
                email     = data['email'],
                password  = data['password'],
            )
            return JsonResponse({'message':'SUCCESS'}, status=200)

        # 기존회원 중복가입 거절
        else:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)




