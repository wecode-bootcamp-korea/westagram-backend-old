import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from . import models


class UserView(View):
    def get(self, request):
        user = models.User.objects.values()
        return JsonResponse({"data": list(user)})

    def post(self, request):
        data = json.loads(request.body)  # POST 데이터 가져오기

        # 이메일이나 패스워드 키가 전달되지 않았을 시, {"message": "KEY_ERROR"}, status code 400 반환
        try:
            email = data["email"]
            password = data["password"]
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        # 회원가입 로직 작성
        models.User(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            userid=data["userid"],
        ).save()
        # 회원가입 성공시 {"message": "SUCCESS"}, status code 200 return
        return JsonResponse({"message": "SUCESS!!"}, status=200)


class LoginView(View):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        # 로그인 로직 작성
        userid = request.POST.get("userid", None)
        password = request.POST.get("password", None)
        if models.User.objects.filter(userid=userid, password=password).exists():
            # 로그인 성공시 {"message": "SUCCESS"}, status code 200 return
            return JsonResponse({"message": "SUCCESS"})
        else:
            # 실패시 {"message": "INVALID_USER"}, status code 401 에러 return
            return JsonResponse({"message": "INVALID_USER"}, status=401)
