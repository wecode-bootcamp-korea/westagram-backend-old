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

        p = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9_]+\.[a-zA-Z-.]+$')
        is_valid_email = True if p.match(email) else False 

        print(is_valid_email)








        