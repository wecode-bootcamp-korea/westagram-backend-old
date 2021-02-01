import json

from django.views import View
from django.http  import JsonResponse

from .models import Accounts


class AccountView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        # 필수사항 미입력시
        try:
            email        = data['email']
            password     = data['password']
            name         = data['name']
            nickname     = data['nickname']
            phone_number = data['phone_number']

            # email, password check
            if email.find('@') == -1 or email.find('.') == -1:
                return JsonResponse({'message': 'email validation'}, status=400)
            if len(password) < 8:
                return JsonResponse({'message': 'password validation'}, status=400)

            # duplicate check
            if Accounts.objects.filter(nickname=nickname) or Accounts.objects.filter(email=email) or Accounts.objects.filter(phone_number=phone_number):
                return JsonResponse({'message': 'input data duplicate'}, status=400)
            
            Accounts.objects.create(
                email        = email,
                name         = name,
                nickname     = nickname,
                password     = password,
                phone_number = phone_number
            )

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        return JsonResponse({'message': 'SUCCESS'}, status=200)


class LoginView(View):
    def get(self, request):
        data = json.loads(request.body)
        
        login_id = ''
        id_type  = ''
        password = ''

        # 3가지중 하나는 있어여 함
        if 'email' in data:
            login_id = data['email']
            id_type  = 'email'
        elif 'nickname' in data:
            login_id = data['data']
            id_type  = 'nickname'
        elif 'phone_number' in data:
            login_id = data['phone_number']
            id_type  = 'phone_number'
        else:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        # password 있는지 확인
        if 'password' in data:
            password = data['password']
        else:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        try:
            # password, login_id check
            if id_type == 'email':
                account = Accounts.objects.get(email=login_id)
            elif id_type == 'phone_number':
                account = Accounts.objects.get(phon_number=login_id)
            elif id_type == 'nickname':
                account = Accounts.objects.get(nickname=login_id)

            if account.password != password:
                return JsonResponse({'message': 'INVALID_USER'}, status=401)
        except:
            return JsonResponse({'message': 'INVALID_USER'}, status=401)

        return JsonResponse({'message': 'SUCCESS'}, status=200)