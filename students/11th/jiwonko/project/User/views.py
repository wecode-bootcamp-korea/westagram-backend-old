import json

from django.views import View
from django.http import JsonResponse

from .models import User

class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if User.objects.filter(email = data['email']).exists():
                return JsonResponse({'message':'Email 중복'}, status = 400)
            elif '@' not in data['email'] and '.' not in data['email']:
                return JsonResponse({'message':'Email @ 미포함'}, status = 400)
            elif len(data['password']) < 8:
                return JsonResponse({'message':'password 8자리 미만 입력'}, status = 400)

            User(
                name = data['name'],
                email = data['email'],
                password = data['password'],
                phone_number = data['phone_number']
            ).save()

            return JsonResponse({'message':'회원가입 완료'}, status = 200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

    def get(self, request):
        user_data = User.objects.values()
        return JsonResponse({'users':list(user_data)}, status = 200)
