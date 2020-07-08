import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from user.models import User
from . import models


class CommentView(View):
    def get(self, request):
        user = models.Comment.objects.values()
        return JsonResponse({"data": list(user)})

    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(id=data["userid"])
        # print(type(user.id), type(user)) # pk 기반으로 save할 경우 쿼리셋을 넘겨준다.
        models.Comment(userid=user, content=data["content"],).save()
        return JsonResponse({"message": "SUCESS!!"})
