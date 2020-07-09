import json

from django.views import View
from django.http  import JsonResponse
from user.models  import User

from . import models


class PostingView(View):
    def post(self, request):
        data = json.loads(request.body)
        # user정보, title 정보가 없을 경우 예외처리
        try:
            post_user = data["user"]
            post_title = data["title"]
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        # 저장 로직
        user = User.objects.get(pk=data["user"])
        models.Posting(
            user=user, 
            title=data["title"], 
            content=data["content"],
        ).save()
        return JsonResponse({"message": "SUCESS!!"})

class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)
        # user or posting key 없을때 예외처리
        try:
            user = User.objects.get(id=data["user"])
            posting = models.Posting.objects.get(id=data["posting"])
        except KeyError
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        models.Comment(
            user=user, 
            posting=posting,
            content=data["content"], ).save()
        return JsonResponse({"message": "SUCESS!!"})
