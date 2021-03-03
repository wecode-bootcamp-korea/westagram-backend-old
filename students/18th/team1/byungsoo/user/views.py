import json

from django.views import View

from .models import User

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        email    = data['email']
        password = data['password']

        

