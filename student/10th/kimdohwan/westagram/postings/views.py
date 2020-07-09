import json

from django.views import View
from django.http import JsonResponse
from user.models import User

from . import models


class PostingView(View):
    def get(self, request):
        return JsonResponse({"page": "posting"})

    def post(self, request):
        data = json.loads(request.body)
        try:
            post_userid = data["userid"]
            post_title = data["title"]
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        # 유효성 검사
        if post_title == None or post_userid == None:
            return JsonResponse({"message": "INVALID_USER OR TITLE"})
        # 저장 로직
        userid = User.objects.get(pk=data["userid"])
        models.Posting(
            userid=userid, 
            title=data["title"], 
            content=data["content"],
        ).save()
        return JsonResponse({"message": "SUCESS!!"})

class CommentView(View):
    def get(self, request):
        user = models.Comment.objects.values()
        return JsonResponse({"data": list(user)})

    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(id=data["userid"])
        posting = models.Posting.objects.get(id=data["posting"])
        models.Comment(userid=user, content=data["content"], posting=posting).save()
        return JsonResponse({"message": "SUCESS!!"})
