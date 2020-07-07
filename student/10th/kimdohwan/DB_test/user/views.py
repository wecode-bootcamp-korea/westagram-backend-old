from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from . import models
import json

# Create your views here.
class UserView(View):
    def get(self, request):
        user = models.User.objects.values()
        return JsonResponse({"data": list(user)})

    def post(self, request):
        data = json.loads(request.body)
        models.User(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            userid=data["userid"],
        ).save()
        return JsonResponse({"message": "SUCESS!!"})


class LoginView(View):
    def get(self, request):
        name = request.GET.get("name")
        # return JsonResponse({"message": "SUCESS!!"})
        return render(request, "user/login.html", {"room": "room"})
