import json

from django.http  import JsonResponse
from django.views import View

from .models import User

class SignUpView(View):
    def post(self, request):

        try:
            data         = json.loads(request.body)
            username     = data['username']
            email        = data['email']
            password     = data['password']
            phone_number = data['phone_number']

            if email == '' or password == '' :
                return JsonResponse({'message': '이메일과 패스워드를 채워주세요' }, status=400)
            elif ('@' and '.') not in email:
                return JsonResponse({'message': '잘못된 형식입니다. 이메일을 다시한번 확인해 주세요'}, status=400)
            elif User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
                return JsonResponse({'message' : '이미 가입되어 있습니다.'}, status=400)
            elif len(password) < 8:
                return JsonResponse({'message': '비밀번호 8자리 이상 입력해 주세요.'}, status=400)
            User.objects.create(username=username, email=email, password=password, phone_number=phone_number)
            return JsonResponse({'message': '회원가입 되었습니다.'}, status=200)
        except :
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):

        try:
            data          = json.loads(request.body)
            user_email    = data['email']
            user_password = data['password']
            user_name     = data['username']
            user_phone    = data['phone_number']

            if user_email == '' and user_name =='' and user_phone == '':
                return JsonResponse({'message':'이메일, 사용자 이름, 핸드폰 번호중 하나를 입력해 주세요.'}, status=400)
            elif user_password == '':
                return JsonResponse({'message':'비밀번호를 채워주세요.'}, status=400)
            else:
                user_data = User.objects.all()
                for user in user_data:
                    if User.objects.filter(username=user_name).exists() or User.objects.filter(email=user_email) or User.objects.filter(phone_number=user_phone):
                        if User.objects.filter(password=user_password):
                            return JsonResponse({'message': 'SUCCESS'}, status=200)
                return JsonResponse({'message': 'INVALID_USER'}, status = 401)
        except:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


 
            
        






 

        
  

