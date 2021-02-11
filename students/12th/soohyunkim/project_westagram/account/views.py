#from django.shortcuts import render

# Create your views here.

import json

from .models import Account

from django.views import View
from django.http import JsonResponse



# 미션2 회원가입뷰 작성
class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        Account(
            username = data["username"],
            email    = data["email"],
            password = data["password"],
            phone    = data["phone"],
        ).save()

        return JsonResponse({ "message" : "회원가입 완료" }, status=200)

