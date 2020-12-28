import json
import re
import bcrypt

from django.http      import JsonResponse
from django.views     import View

from user.models  import User


# 회원가입시 닉넴임, 이메일, 전화번호 셋 중 하나를 account 라는 속성으로 받는다고 가정
class SignUpView(View):
    def post(self, request):
        # 1. account, password 꺼내기, 필수 값 확인
        request_body = json.loads(request.body)
        try:
            account      = request_body['account']
            password     = request_body['password']
            name         = request_body['name']
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        # 2. 받은 값들에 대한 validation 및 account type 확인
        REGEX_PASSWORD = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%^*#?&])[A-Za-z\d$@$!%^*#?&]{8,20}$")
        if not REGEX_PASSWORD.match(password):
            return JsonResponse({"MESSAGE": "INVALID_INPUT"}, status=400)

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

        # 3. Unique 이어야 하는 값들에 대한 중복 검사
        if account_type == "nick_name":
            if User.objects.filter(nick_name=account).exists():
                return JsonResponse({"MESSAGE": "NAME_DUPLICATION"}, status=400)
        elif account_type == "email":
            if User.objects.filter(email=account).exists():
                return JsonResponse({"MESSAGE": "EMAIL_DUPLICATION"}, status=400)
        elif account_type == "phone_number":
            if User.objects.filter(phone_number=account).exists():
                return JsonResponse({"MESSAGE": "PHONE_NUMBER_DUPLICATION"}, status=400)

        # 4. 패스워드 암호화
        hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode()

        # 5. 모든 조건 통과하면 DB 에 저장
        if account_type == "email":
            user                = User.objects.create(
                name            = name,
                email           = account,
                hashed_password = hashed_password,
            )
        elif account_type == "phone_number":
            user = User.objects.create(
                name            = name,
                phone_number    = account,
                hashed_password = hashed_password,
            )
        elif account_type == "nick_name":
            user = User.objects.create(
                name            = name,
                nick_name       = account,
                hashed_password = hashed_password,
            )

        # 6. DB에 저장되면 성공 코드 리턴
        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)


