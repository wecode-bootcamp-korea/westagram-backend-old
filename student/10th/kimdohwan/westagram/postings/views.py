import json

from django.views import View
from django.http  import JsonResponse
from user.models  import User

from . import models


class PostingView(View):
    def get(self, request):
        return JsonResponse({"page": "posting"})

    def post(self, request):
        data = json.loads(request.body)
        try:
            post_user = data.get("user",None)
            post_title = data.get("title",None)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
        # 유효성 검사
        if post_title == None or post_user == None:
            return JsonResponse({"message": "INVALID_USER OR TITLE"})
        # 저장 로직
        user = User.objects.get(pk=data["user"])
        models.Posting(
            user=user, 
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
        user = User.objects.get(id=data["user"])
        posting = models.Posting.objects.get(id=data["posting"])
        models.Comment(
            user=user, 
            content=data["content"], 
            posting=posting).save()
        return JsonResponse({"message": "SUCESS!!"})
