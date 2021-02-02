import json
from json.decoder import JSONDecodeError
import re

from django.http import JsonResponse, HttpResponse
from django.views import View


from user.models import User

MINIMUM_PASSWORD_LENGTH = 8

class SignUpView(View):
    def post(self, request):

        try:
            data = json.loads(request.body)

            check_lst = ['name', 'user_name', 'email', 'password', 'phone_number']
            for key in check_lst:
                if key not in data.keys():
                    return JsonResponse({'message':'KEY_ERROR'}, status=400)

            for value in data.values():
                if not value:
                    return JsonResponse({'message': 'KEY_ERROR'}, status=400)

            if not '@' in data['email'] or not '.' in data['email']:
                return JsonResponse({'message':'The email is not valid'}, status=400)

            if not MINIMUM_PASSWORD_LENGTH <= len(data['password']):
                return JsonResponse({'message': 'The password is not valid'}, status=400)

            user = User.objects.filter(email=data['email'])
            if not user:
                User.objects.create(
                    name      = data['name'],
                    user_name = data['user_name'],
                    email     = data['email'],
                    password  = data['password'],
                )
                return JsonResponse({'message':'SUCCESS'}, status=200)

            else:
                return JsonResponse({'message':'USER_ALREADY_EXIST'}, status=409)

        except JSONDecodeError:
            return JsonResponse({'message':'The request is not valid'}, status=400)


class SignInView(View):
    def post(self, request):

        try:
            data = json.loads(request.body)

            check_lst_id = ['user_name', 'email', 'phone_number']
            check = check_lst_id[:]
            login_id = ''
            for key in check_lst_id:
                if key in data.keys():
                    login_id = key
                    break
                elif not check:
                    return JsonResponse({'message': 'KEY_ERROR'}, status=400)
                else:
                    check.remove(key)

            check_lst_pw = 'password'
            if check_lst_pw not in data.keys():
                return JsonResponse({'message':'KEY_ERROR'}, status=400)

            for value in data.values():
                if not value:
                    return JsonResponse({'message': 'KEY_ERROR'}, status=400)

            user = User.objects.filter(user_name=data[login_id]) | User.objects.filter(email=data[login_id]) | User.objects.filter(phone_number=data[login_id])
            user = user.first()
            if user:
                if (data[login_id] == user.user_name or data[login_id] == user.email or data[login_id] == user.phone_number) and data['password'] == user.password:
                    return JsonResponse({'message': 'SUCCESS'}, status=200)

                else:
                    return JsonResponse({'message':'The account is not valid'}, status=400)

            else:
                return JsonResponse({'message':'User_Does_Not_Exist'}, status=400)

        except JSONDecodeError:
            return JsonResponse({'message':'The request is not valid'}, status=400)
