import json

from django.http  import JsonResponse
from django.views import View

from .models import User


class SignupView(View):

    def post(self,request):
        
        #reqeust 에서  body 만 필요해서 가져오고, 파이썬으로 loads 해서 변수저장.
        signup_data = json.loads(request.body)

        '''
        프론트에서 오는 json 바디는 이렇게 오겟징?
          signup_data ={
                "user": jojoojo
                "email" : ~~~~~.com
                "password" : 123456778
          }
        '''

        # 저장된 변수들을 키로 불러와서 또 변수에 each 저장.
        username     = signup_data['username']
        email        = signup_data['email']
        password     = signup_data['password']

            # 에러 필터링 로직 구현.
        try:
                # 이미 가입한 유저가 회원가입을 시도할 때   
            if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
                return JsonResponse({'message': 'Account with the same username or email already exists.'}, status = 400)
            
            # 계정(이메일, 아이디)의 형식이 맞지 않을 때(email validation)
            elif '@' and '.' not in email:
                return JsonResponse({'message': 'Please submit a valid email address.'}, status = 400)
            
            # 비밀번호의 형식이 맞지 않을 때
            elif len(str(password)) < 8:
                return JsonResponse({'message': 'Please submit a valid password.'}, status = 400)
            
            # 정상적인 입력시 create 쿼리를 날린다. 리턴 위에 쿼리를 날려야 잘 생성된다.
            User.objects.create(
                
                username = signup_data['username'],
                email    = signup_data['email'],
                password = signup_data['password']
            )
            return JsonResponse({'message': 'SUCCESS'}, status = 200)

        except:
            # key error
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

class LoginView(View):

    def post(self,request):   

        #reqeust 에서  body 만 필요해서 가져오고, 파이썬으로 loads 해서 변수저장.
        login_data = json.loads(request.body)

        '''
        프론트에서 오는 json 바디는 이렇게 오겟징?
          login_data ={
                "email" : ~~~~~.com
                "password" : 123456778
          }
        '''

        # 저장된 변수들을 키로 불러와서 또 변수에 each 저장.
        email = login_data['email']
        password = login_data['password']

        # 에러 필터링 로직 구현.
        try:
            # 계정이 틀릴때 or 패스워드 틀릴때 . filter() 메소드에 **kargs 로 한번에 여러개 컬럼 데이터 필터 가능.
            if not User.objects.filter(email=email, password=password).exists() :
                return JsonResponse({'message': 'Please enter correct email and password.'}, status = 400)

            # 정상적인 입력시
            return JsonResponse({'message': 'SUCCESS'}, status = 200)

        except:
            # key error
            return JsonResponse({'message': 'INVALID_USER'}, status = 401)

