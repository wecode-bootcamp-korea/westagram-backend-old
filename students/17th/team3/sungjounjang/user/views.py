import json

from django.views import View
from django.http  import JsonResponse
import bcrypt

from .models import Accounts


class AccountView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        # 필수사항 미입력시
        try:
            email        = data['email']
            password     = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            name         = data['name']
            nickname     = data['nickname']
            phone_number = data['phone_number']

            print('-----------------------------------')
            print(password)

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
    def post(self, request):
        data = json.loads(request.body)

        try:
            email        = data.get('email')
            nickname     = data.get('nickname')
            phone_number = data.get('phone_number')
            password     = data['password']

            # password, login_id check
            if email:
                account = Accounts.objects.get(email=email)
            if nickname:
                account = Accounts.objects.get(nickname=nickname)
            if phone_number:
                account = Accounts.objects.get(phone_number=phone_number)

            if not bcrypt.checkpw(password.encode('utf-8'), account.password):
                return JsonResponse({'message': 'INVALID_USER'}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        return JsonResponse({'message': 'SUCCESS'}, status=200)