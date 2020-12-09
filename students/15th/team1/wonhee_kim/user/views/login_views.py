import re
import jwt
import json
import bcrypt
from datetime     import datetime, timedelta

from django.http  import JsonResponse
from django.views import View

from user.models  import User
from westargram   import my_settings


class LogInView(View):
    def post(self, request):
        print()
        print("================= 로그인 절차 기동 =================")
        # 1. 아이디 패스워디 꺼내기, 필수 값 확인
        try:
            request_body = json.loads(request.body)
            account      = request_body['account']
            password     = request_body['password']
        except Exception as e:
            print(f'e: {e}')
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        # 2. 받은 값들에 대한 validation 및 account type 확인(프론트에서 account_type을 지정해주지 않는다고 가정)
        email_regex                    = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        email_check                    = re.match(email_regex, account)
        phone_number_regex             = re.compile(r'^\d{3}-\d{3,4}-\d{4}$')
        phone_number_check             = re.match(phone_number_regex, account)
        phone_number_regex_only_number = re.compile(r'^\d{10,11}$')
        phone_number_check_only_number = re.match(phone_number_regex_only_number, account)
        nick_name_regex                = re.compile(r'^(?=.*[a-zA-Z])(?=.*[!@#$%^~*+=-_])(?=.*[0-9]).{5,20}$')
        nick_name_check                = re.match(nick_name_regex, account)

        if email_check:
            account_type = "email"
        elif phone_number_check:
            account      = account.replace("-", "")
            account_type = "phone_number"
        elif phone_number_check_only_number:
            account_type = "phone_number"
        elif nick_name_check:
            account_type = "nick_name"
        else:
            return JsonResponse({"MESSAGE": "INVALID_INPUT"}, status=400)

        # 3. 계정이 존재하는지 검사
        try:
            if account_type   == "nick_name":
                account = User.objects.get(nick_name=account)
            elif account_type == "email":
                account = User.objects.get(email=account)
            elif account_type == "phone_number":
                account = User.objects.get(phone_number=account)
        except Exception as e:
            print(f'e: {e}')
            return JsonResponse({'MESSAGE': 'INVALID_INPUT'}, status=401)

        # 4. 계정에 대한 패스워드가 일치하는지 검사
        password_check = bcrypt.checkpw(password.encode('UTF-8'), account.hashed_password.encode('UTF-8'))
        if not password_check:
            return JsonResponse({'MESSAGE': 'INVALID_INPUT'}, status=401)

        # 5. 모든 조건 통과하면 토큰(24시간 동안 유효) 발급하여 로그인 처리
        user_id = account.id
        payload = {
            'user_id': user_id,
            'exp'    : datetime.utcnow() + timedelta(seconds  =60 * 60 * 24)
        }
        token = jwt.encode(payload, my_settings.SECRET_KEY, algorithm=my_settings.encryption_algorithm)
        print("================= 로그인 정상 종료 =================")
        return JsonResponse({'MESSAGE'     : 'SUCCESS',
                             'ACCESS_TOKEN': token.decode('UTF-8')
                             }, status=200)
