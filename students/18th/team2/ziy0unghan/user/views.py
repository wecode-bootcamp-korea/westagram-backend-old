import json

from django.http  import JsonResponse
from django.views import View

from .models import User

class SignUpView(View):
    def post(self, request):

        data = json.loads(request.body)
        username     = data['username']
        email        = data['email']
        password     = data['password']
        phone_number = data['phone_number']

        if username == ''or email == '' or password == '' or phone_number == '':
            return JsonResponse({'message': 'KEY_ERROR' }, status=400)
        elif ('@' and '.') not in email:
            return JsonResponse({'message': '잘못된 형식입니다.'}, status=400)
        elif len(password) < 8:
            return JsonResponse({'message': '비밀번호 8자리 이상 입력해 주세요.'}, status=400)
        elif data in User.objects.filter(email=email) or User.objects.filter(password=password):
            return JsonResponse({'message' : '이미 가입된 계정입니다.'}, status=401)
        else:
            User.objects.create(username=username, email=email, password=password, phone_number=phone_number)
            return JsonResponse({'message': '회원가입 되었습니다.'}, status=200)

class SignInView(View):
    def post(self, request):

        data          = json.loads(request.body)
        user_email    = data['email']
        user_password = data['password']
        user_name     = data['username']
        user_phone    = data['phone_number']

        #이메일,유저네임,핸드폰번호 중 하나라도 기입, 기입안하면 키에러
        #패스워드 입력 안하면 키에러
        if user_email == '' and user_name =='' and user_phone == '':
            if user_password == '':
                return JsonResponse({'message':'KEY_ERROR'}, status=400)
        else: # 가입된 유저 확인
            user_data     = User.objects.all()
            for user in user_data:
                if user_name == user.username or user_email == user.email or user_phone == user.phone_number:
                    if user_password == user.password:
                        return JsonResponse({'message': 'SUCCESS'}, status=200)
                return JsonResponse({'message': 'INVALID_USER'}, status = 401)

 
            
        






 

        
  

