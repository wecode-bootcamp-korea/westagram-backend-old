import json

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from . import models

class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email = data["email"]
            password = data["password"]
            if "@" not in email or len(password) <= 4:
                return JsonResponse({"message": "VALIDATION ERROR"}, status=400)
            models.User(
                name=data["name"],
                email=data["email"],
                password=data["password"],
                userid=data["userid"],
            ).save()
            return JsonResponse({"message": "SUCESS"}, status=200)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            userid = data['userid']
            password = data['password']
            if models.User.objects.filter(userid=userid, password=password).exists():
                return JsonResponse({"message": "SUCESS"},status=200)
            else:
                return JsonResponse({"message": "INVALID_USER"}, status=401)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class FollowView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            from_user = models.User.objects.get(pk=data["from_user"])
            to_user = models.User.objects.get(pk=data["to_user"])
            if from_user == to_user:
                return JsonResponse({"message": "SAME USER"}, status=400)
            pk = models.Follow.objects.filter(from_user=from_user, to_user=to_user)
            if pk.exists():
                pk.update(is_follow=data["is_follow"])
                return JsonResponse({"message": "SUCESS UPDATE "},status=200)
            else:
                models.Follow(
                    from_user=from_user,
                    to_user=to_user,
                    is_follow=data["is_follow"]
                ).save()
                return JsonResponse({"message": "SUCESS"}, status=200)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)