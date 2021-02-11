import re
import jwt
import json
import bcrypt
from datetime     import datetime, timedelta

from django.http  import JsonResponse
from django.views import View

from user.models  import User
from westargram.my_settings import SECRET_KEY, ENCRYPTION_ALGORITHM


class LogInView(View):
    def post(self, request):
        # 1. 아이디 패스워디 꺼내기, 필수 값 확인
        request_body = json.loads(request.body)
        try:
            account      = request_body['account']
            password     = request_body['password']
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        # 2. 받은 값들에 대한 validation 및 account type 확인(프론트에서 account_type을 지정해주지 않는다고 가정)
        REGEX_EMAIL                    = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        REGEX_PHONE_NUMBER_WITH_HYPHEN = re.compile(r'^\d{3}-\d{3,4}-\d{4}$')
        REGEX_PHONE_NUMBER             = re.compile(r'^\d{10,11}$')
        REGEX_NICK_NAME                = re.compile(r'^(?=.*[a-zA-Z])(?=.*[!@#$%^~*+=-_])(?=.*[0-9]).{5,20}$')

        if REGEX_EMAIL.match(account):
            account_type = "email"
        elif REGEX_PHONE_NUMBER.match(account):
            account_type = "phone_number"
        elif REGEX_PHONE_NUMBER_WITH_HYPHEN:
            account      = account.replace("-", "")
            account_type = "phone_number"
        elif REGEX_NICK_NAME:
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
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': 'USER_NOT_EXIST'}, status=400)

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
        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ENCRYPTION_ALGORITHM)

        return JsonResponse({'MESSAGE'     : 'SUCCESS',
                             'ACCESS_TOKEN': access_token.decode('UTF-8')
                             }, status=200)
