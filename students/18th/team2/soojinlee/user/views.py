import json
from django.http import JsonResponse

from django.views import View
from .models import User


class UserSignup(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        user_name = data['user_name']
        phone_number = data['phone_number']
        pw = data['pw']

        if email == '' and pw == '':
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        elif '@' not in email and '.' not in email:
            return JsonResponse({'message': 'email을 확인하세요'}, status=400)
        elif len(pw) < 8:
            return JsonResponse({'message': 'pw는 8자리 이상으로 해야합니다.'}, status=400)
        else:
            repeated_info = User.objects.filter(email=email) | User.objects.filter(
                user_name=user_name) | User.objects.filter(phone_number=phone_number)
            for info in repeated_info:
                if user_name == info.user_name:
                    return JsonResponse({'message': '이미 있는 user_name입니다.'}, status=400)
                elif email == info.email:
                    return JsonResponse({'message': '이미 있는 email입니다.'}, status=400)
                elif phone_number == info.phone_number:
                    return JsonResponse({'message': '이미 있는 phone_number'}, status=400)

            User.objects.create(email=data['email'], pw=data['pw'],
                                user_name=data['user_name'], phone_number=data['phone_number'])
            return JsonResponse({'message': 'SUCCESS'}, status=200)


class UserLogin(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        user_name = data['user_name']
        phone_number = data['phone_number']
        pw = data['pw']
        user = User.objects.all()

        if user_name == '' or phone_number == '' or email == '':
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        elif pw == '':
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        for users in user:
            if user_name == users.user_name or phone_number == users.phone_number or email == users.email:
                if pw == users.pw:
                    return JsonResponse({'message': 'SUCCESS'}, status=200)
            continue

            if user_name != users.user_name or phone_number != users.phone_number or email != users.email:
                return JsonResponse({'message': "INVALID_USER"}, status=401)
