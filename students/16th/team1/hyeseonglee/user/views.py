import json
import re
import bcrypt
import jwt

from django.http             import JsonResponse
from django.views            import View
from django.db.models        import Q  
from django.core.validators  import validate_email, ValidationError
from django.utils.decorators import method_decorator

from user.models             import User
from westagram.my_settings   import SECRET, ALGORITHM
from user.decorator          import login_decorator

auth = [login_decorator,]


class SignUpView(View):
    def post(self, request):
        try:
            data        = json.loads(request.body)
            email       = data['email']
            password    = data['password']
            MIN_LEN_PWD = 8

            if User.objects.filter(email=data['email']):
                return JsonResponse({'MESSAGE':'이미 존재하는 이메일입니다.'}, status=400)
           
            if len(password) < MIN_LEN_PWD:  
                return JsonResponse({'MESSAGE':f'비밀번호는 {MIN_LEN_PWD}자 이상으로 설정 하세요.'}, status=400)

            try:
                validate_email(email) 
            except ValidationError:   
                return JsonResponse({'MESSAGE':'유효한 이메일이 아닙니다!'}, status=400)

            hash_pwd = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode() # 디코드 메서드 전까지는 바이트 값이고 이후 decode()를 통해서 byte-> string 참고. 암호 복원이 아니에요.

            User.objects.create(
                                password=hash_pwd,
                                email   =email                              
                                )
            return JsonResponse({'MESSAGE':'계정 생성 성공!'}, status=201)
            
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY 에러 발생!'},status=400)

        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE 에러 발생!'},status=400)
            
        

@method_decorator(auth, name='dispatch')
class LoginView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            password = data['password']
            user = User.objects.get(email=data['email'])

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')): # 첫번째 브라우저로부터 가져온 값을 바이트로 바꾸고, 2번째인자는 db의 해싱된 문자열을 바이트로 비교해서 두값을 확인하여 True, False
                user_token = jwt.encode({'user_id': user.id}, SECRET, algorithm=ALGORITHM)
                return JsonResponse({'MESSAGE':'액세스 토큰 생성 성공!','엑세스 토큰': user_token}, status=200)
            return JsonResponse({'MESSAGE':'비밀번호를 다시 확인해주세요'}, STATUS=400)
            
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY 에러 발생!'},status=400)

        except ValueError:
            return JsonResponse({'MESSAGE': 'VALUE 에러 발생!'},status=400)
