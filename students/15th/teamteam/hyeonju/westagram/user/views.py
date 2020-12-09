#from django.shortcuts import render

import json
import re
from django.views import View
from django.http import JsonResponse
from .models import Signup

# Create your views here.
class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        email_validation = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        pw_validation = '^[A-Za-z0-9@#$%^&+=]{8,}$'

        try:

            if not re.match(email_validation, data['email']):
                return JsonResponse(
                    {"message":"INVALID_ID"}, status = 401
                    )

            if not re.match(pw_validation, data['password']):
                return JsonResponse(
                    {"message":"INVALID_PW"}, status = 400
                    )


            if Signup.objects.filter(email=data['email']).exists():
                return JsonResponse(
                    {"message":"USER_EXIST"}, status = 400
                    )

            else:
                Signup.objects.create(
                    email = data['email'],
                    password = data['password']
                    )
                return JsonResponse({'message': 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)

