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
        # print(post_userid, post_title, data)
        if post_title == None or post_userid == None:
            return JsonResponse({"message": "INVALID_USER OR TITLE"})
        # 저장 로직
        userid = User.objects.get(pk=data["userid"])
        models.Posting(
            userid=userid, title=data["title"], content=data["content"],
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
        # print(type(user.id), type(user)) # pk 기반으로 save할 경우 쿼리셋을 넘겨준다.
        models.Comment(userid=user, content=data["content"], posting=posting).save()
        return JsonResponse({"message": "SUCESS!!"})


# http -v http://127.0.0.1:8000/user/posting userid="1" title="포스팅 제목1" content="포스팅 내용"
# http -v http://127.0.0.1:8000/user/comment userid="1" posting="1" content="댓글 내용 !!"
