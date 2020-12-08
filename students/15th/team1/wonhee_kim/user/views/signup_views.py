import json
import re
import bcrypt

from django.http      import JsonResponse
from django.views     import View

from user.models  import User


# 회원가입시 닉넴임, 이메일, 전화번호 셋 중 하나를 account 라는 속성으로 받는다고 가정
class SignUpView(View):
    def post(self, request):
        print()
        print("================= 회원가입 절차 기동 =================")
        # 1. account, password 꺼내기, 필수 값 확인
        try:
            request_body = json.loads(request.body)
            account      = request_body['account']
            password     = request_body['password']
            name         = request_body['name']
        except Exception as e:
            print(f'e: {e}')
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        # 2. 받은 값들에 대한 validation 및 account type 확인
        password_regex = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%^*#?&])[A-Za-z\d$@$!%^*#?&]{8,20}$")
        password_check = re.match(password_regex, password)
        if not password_check:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

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
            account = account.replace("-", "")
            account_type = "phone_number"
        elif phone_number_check_only_number:
            account_type = "phone_number"
        elif nick_name_check:
            account_type = "nick_name"
        else:
            return JsonResponse({"MESSAGE": "NO_ACCOUNT"}, status=400)

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

        # 5. 모든 조건 통과하면 DB 에 저장 시도
        try:
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
        except Exception as e:
            print(f'e: {e}')
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

        # 6. DB에 저장되면 성공 코드 리턴
        print("================= 회원가입 정상 종료 =================")
        return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)


