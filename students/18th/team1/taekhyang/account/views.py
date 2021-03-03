import json
import re

from django.views     import View
from django.http      import JsonResponse


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
        is_valid_password = True if p_password.match(email) else False

        if not is_valid_email or not is_valid_password:
            return JsonResponse({'message': 'WRONG_FORMAT'}, status=400)

        return JsonResponse({'message': 'SUCCESS'}, status=200)