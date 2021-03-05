import json

from django.http  import JsonResponse
from django.views import View

from .models import User

class SignUpView(View):
    def post(self, request):

            #이메일 패스워드 확인
            data = json.loads(request.body)

            username     = data['username']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']

            if username == ''or email == '' or password == '' or phone_number == '':
                return JsonResponse({'message': 'KEY-ERROR' }, status=400)
            elif ('@' or '.') not in email:
                return JsonResponse({'message': '잘못된 형식입니다.'}, status=400)
            elif len(password) < 8:
                return JsonResponse({'message': '비밀번호 8자리 이상 입력해 주세요.'}, status=400)
            elif data in User.objects.filter(email=email) or User.objects.filter(password=password):
                return JsonResponse({'message' : '이미 가입된 계정입니다.'}, status=401)
            else:
                User.objects.create(username=username, email=email, password=password, phone_number=phone_number)
                return JsonResponse({'message': '회원가입 되었습니다.'}, status=200)

 

        
  

