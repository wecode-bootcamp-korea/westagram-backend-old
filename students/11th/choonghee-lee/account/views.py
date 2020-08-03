import json
import re

from django.db.models     import Q
from django.http          import JsonResponse
from django.views.generic import View

from .models import User

class SignUpView(View):
    def post(self, request):
        # json 형식 체크
        try:
            data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message': 'INVALID_JSON'}, status=400)

        # key 체크
        try:
            username = data['username']
            email    = data['email']
            phone    = data['phone']
            password = data['password']
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        # value 체크
        if not username and not email and not phone:
            return JsonResponse({'message': 'INVALID_USERNAME'}, status=400)

        # 이메일 체크
        EMAIL_REGEX = "^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$"
        if email and re.search(EMAIL_REGEX, email):
            return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)

        # 패스워드 체크
        if len(password) < 8:
            return JsonResponse({'message': 'INVALID_PASSWORD'}, status=400)

        # 중복 체크
        try:
            duplicated_user = User.objects.get(
                Q(username = username) | Q(email = email) | Q(phone = phone)
            )
        except:
            User(
                username = username,
                email    = email,
                phone    = phone,
                password = password,
            ).save()
            return JsonResponse({'message': 'SUCCESS'}, status=200)
        else:
            return JsonResponse({'message': 'ALREADY_SIGNED_UP_USER'}, status=401)