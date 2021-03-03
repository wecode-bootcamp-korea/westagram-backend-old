import json
import re

from django.views     import View
from django.http      import JsonResponse

from .models import User


class SignUpView(View):
    def post(self, request):
        data      = request.body
        json_data = json.loads(data)

        email    = json_data['email']
        password = json_data['password']

        if not email or not password:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        p_email    = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9_]+\.[a-zA-Z-.]+$')
        p_password = re.compile(r'.{8,45}')

        # TODO : modify password validation check
        is_valid_email    = True if p_email.match(email) else False 
        is_valid_password = True if p_password.match(password) else False

        if not is_valid_email or not is_valid_password:
            return JsonResponse({'message': 'INVALID_FORMAT'}, status=400)

        # check existing user
        is_existing_user = True if User.objects.filter(email=email) else False
        if is_existing_user:
            return JsonResponse({'message': 'EXISTING_USER'}, status=400)

        # not sure if it may throw unexpected error when inserting data
        try:
            User.objects.create(email=email, password=password)
        except:
            return JsonResponse({'message': 'INVALID_FORMAT'}, status=400)
        return JsonResponse({'message': 'SUCCESS'}, status=200)