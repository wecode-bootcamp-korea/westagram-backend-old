import json
import re # regular expression
import bcrypt
import jwt

from json               import JSONDecodeError
from django.http        import JsonResponse
from django.shortcuts   import get_object_or_404
from django.views       import View
from django.core.exceptions import ObjectDoesNotExist
from westagram.settings import SECRET_KEY

from .models import User

# sign up

class SignUp(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except JSONDecodeError:
            return JsonResponse({"message":"JSONDecodeError"}, status=400)
        
        # ## 이메일이나 패스워드 키가 전달되지 않았을 시, {"message": "KEY_ERROR"}, status code 400 을 반환
        # try:
        #     #data_email = data['email'] # 휴대번호 또는 이메일
        #     data_email = data.get('email','None') # 휴대번호 또는 이메일
        #     data_name =  data.get('name', 'None') # 성명
        #     data_username = 'default_name' # 사용자이름
        #     data_password = data['password'] # 비밀번호
        # except KeyError:
        #     return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
        # if 문으로 try except 대체할 수 있으면, if문으로 대체 : 부하 훨씬 적음
        chk = 0
        for key in data:
            if key == 'email' or key =='password':
                chk+=1
        if chk < 2:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        
            
        


        #회원가입시 이메일을 사용할 경우, 이메일에는 @와 .이 필수로 포함. 없으면 적절한 에러를 반환 (email validation)
        # 이메일인지 휴대번호인지 체크
        try:
            email_chk = int(data_email) 
        except ValueError:  # 이메일이면 형변환에서 에러발생
            email_re = re.compile('..*[@]..*[.]..*')
            if not email_re.match(data_email):
                return JsonResponse({"message": "EMAIL_VALIDATION_ERROR"}, status=400)

        #회원가입시 비밀번호는 8자리 이상. 해당 조건이 만족되지 않을 시, 적절한 에러를 반환 (password validation)
        if len(data_password) < 8:
            return JsonResponse({"message": "PASSWORD_VALIDATION_ERROR"}, status=400)

        #회원가입시 전화번호, 사용자 이름, 이메일이 기존에 존재하는 자료와 중복되어서는 안됩니다. 
        email_duplication_chk    = User.objects.filter(email=data_email).values()
       # username_duplication_chk = User.objects.filter(username=data_username).values()

        # 비밀번호 암호화
        encrypted_pw = bcrypt.hashpw(data_password.encode('utf-8'), bcrypt.gensalt())
        

        if email_duplication_chk :
            return JsonResponse({"message": "EAMIL_ALREADY_EXISTS"}, status=400)
        #elif username_duplication_chk:
        #    return JsonResponse({"message": "USERNAME_ALREADY_EXISTS"}, status=400)
        else:
            # 회원가입이 성공하면 {"message": "SUCCESS"}, status code 200을 반환합니다.
            User(
                email = data_email,
                name = data_name,
                username = data_username,
                password = encrypted_pw.decode('utf-8')
            ).save()
      
      
            return JsonResponse({'message':'SUCCESS'}, status=200)

class SignIn(View):
    def post(self, request):
        # 인스타그램에 로그인 할 때에는 전화번호, 사용자 이름 또는 이메일이 필수로 필요합니다.
        # 인스타그램에 로그인 할 때에는 비밀번호가 필수로 필요합니다.
        # 계정이나 패스워드 키가 전달되지 않았을 시, {"message": "KEY_ERROR"}, status code 400 을 반환
        try:
            data = json.loads(request.body)
        except JSONDecodeError:
            return JsonResponse({"message":"JSONDecodeError"}, status=400)

        # try:
        #     data_email = data['email']
        #     data_password = data['password']
        # except KeyError:
        #     return JsonResponse({"message": "KEY_ERROR"}, status=400)
        # if 문으로 try except 대체할 수 있으면, if문으로 대체 : 부하 훨씬 적음
        chk = 0
        for key in data:
            if key == 'email' or key =='password':
                chk+=1
        if chk < 2:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
            
        # 계정이 존재하지 않을 때, {"message": "INVALID_USER"}, status code 401을 반환
        try:
            get_user_info = User.objects.get(email=data_email)
        except ObjectDoesNotExist: # 로그인을 위해 전화번호 또는 이메일 대신 '사용자 이름'을 입력한 경우
            try:
                get_user_info = User.objects.get(username=data_email)
            except ObjectDoesNotExist: # 전화번호, 이메일, 사용자이름 모두 다 등록 되지 않은 경우
                return JsonResponse( {"message": "INVALID_USER"}, status=401)
        
        
        # 로그인이 성공하면 토큰발행, status code 200을 반환
        if  bcrypt.checkpw(data_password.encode('utf-8'), get_user_info.password.encode('utf-8')):
            token = jwt.encode({'user_id': get_user_info.id}, SECRET_KEY, algorithm='HS256')
            return JsonResponse({'access_token':token.decode('utf-8')}, status = 200)
        else: #비밀번호가 맞지 않을 때, {"message": "WRONG_PASSWORD"}, status code 401을 반환
            return JsonResponse({"message": "WRONG_PASSWORD"}, status=401)
        
     