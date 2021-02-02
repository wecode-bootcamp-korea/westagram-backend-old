import json
from json.decoder import JSONDecodeError
import re

from django.db.models import Q
from django.http      import JsonResponse, HttpResponse
from django.views     import View

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

            user_name    = data.get('user_name', None)
            email        = data.get('email', None)
            password     = data.get('password', None)
            phone_number = data.get('phone_number', None)

            if not (user_name or email or phone_number) and not password:
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

            if User.objects.filter(Q(user_name=user_name) | Q(email=email) | Q(phone_number=phone_number)).exists():

                if User.objects.filter(password=password):
                    return JsonResponse({'message': 'SUCCESS'}, status=200)

                else:
                    return JsonResponse({'message': 'INVALID_ACCOUNT'}, status=401)

            else:
                return JsonResponse({'message': 'INVALID_ACCOUNT'}, status=401)

        except JSONDecodeError:
            return JsonResponse({'message': 'BAD_REQUEST'}, status=400)