from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
from . import models


class UserView(View):
    def get(self, request):
        user = models.User.objects.values()
        return JsonResponse({"data": list(user)})

    def post(self, request):
        data = json.loads(request.body)
        print(data)
        models.User(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            userid=data["userid"],
        ).save()
        return JsonResponse({"message": "SUCESS!!"})


class LoginView(View):
    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        userid = request.POST.get("userid", None)
        password = request.POST.get("password", None)

        if models.User.objects.filter(userid=userid, password=password).exists():
            return HttpResponse(status=200)
        else:
            return JsonResponse({"message": "INVALID_USER"}, status=401)
