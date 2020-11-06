import json
from django.views import View
from django.http  import JsonResponse
from .models import User
from django.db.models import Q

class SignUpView(View):
    def post(self, request):
        PASSWORD_MINIMUN_LENGTH = 8
        NECESSERY_KEYS = ('name', 'email', 'phone_number', 'password')

        data = json.loads(request.body)

        for k in NECESSERY_KEYS:
            if k not in data.keys():
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        if len(data['password']) < PASSWORD_MINIMUN_LENGTH:
            return JsonResponse({'message': 'PASSWORD_VALIDATION'}, status=400)

        if 'email' in data:
            if '@' not in data['email'] or '.' not in data['email']:
                return JsonResponse({'message': 'EMAIL_VALIDATION'}, status=400)

        if User.objects.filter(  Q(name        =data['name']) \
                               | Q(email       =data['email']) \
                               | Q(phone_number=data['phone_number'])).exists():
            return JsonResponse({'message':'DATA_ALREADY_EXIST'}, status=400)

        User.objects.create(
            name        =data['name'],
            password    =data['password'],
            email       =data['email'],
            phone_number=data['phone_number']
        )

        return JsonResponse({'message': 'SUCCESS'}, status=200)

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

