import json
from django.views import View
from django.http  import JsonResponse
from .models import User
from django.db.models import Q
import re
import bcrypt
class SignUpView(View):
    def post(self, request):
        PASSWORD_MINIMUN_LENGTH = 8
        NECESSERY_KEYS = ('name', 'email', 'phone_number', 'password')

        password_re = re.compile('^[A-Za-z0-9]{8,}$')
        email_re    = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
#1. 패스워드 정규식 검사 추가
#2. 인증 추가 패스워드 저장 확인
#
        data = json.loads(request.body)

        for k in NECESSERY_KEYS:
            if k not in data.keys():
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        if password_re.match(data['password']) == None:
            return JsonResponse({'message': 'PASSWORD_VALIDATION'}, status=400)

        if email_re.match(data['email']) == None:
            return JsonResponse({'message': 'EMAIL_VALIDATION'}, status=400)

        if User.objects.filter(  Q(name        =data['name']) \
                               | Q(email       =data['email']) \
                               | Q(phone_number=data['phone_number'])).exists():
            return JsonResponse({'message':'DATA_ALREADY_EXIST'}, status=400)

        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        User.objects.create(
            name        =data['name'],
            password    =hashed_password.decode('utf-8'),
            email       =data['email'],
            phone_number=data['phone_number']
        )

        return JsonResponse({'message': 'SUCCESS'}, status=201)

class LoginView(View):
    def post(self, request):

        data = json.loads(request.body)
        NECESSERY_KEYS = ('account', 'password')
        account_key = ''

        for k in NECESSERY_KEYS:
            if k not in data.keys():
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        try:
            user = User.objects.get(  Q(name        =data['account']) \
                                    | Q(email       =data['account']) \
                                    | Q(phone_number=data['account']))

            if data['password'] == user.password:
                return JsonResponse({'message': 'SUCCESS'}, status=200)
            else:
                return JsonResponse({'message':'INVALID_USER'}, status=401)

        except Exception as ex:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

