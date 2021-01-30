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
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
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

        return JsonResponse({'message': 'SUCCESS'}, status=200)


