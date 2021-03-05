import json, re

from django.views import View
from django.http  import JsonResponse

from .models     import Post, Image
from user.models import User

class PostView(View):
    def get(self, request):
        

    def post(self, request):
        data = json.loads(request.body)

        # 사용자가 보낸 정보를 각 변수에 담기
        user_email = data["user"] # ex) dhnp6803@naver.com
        image_url  = data["image_url"] # ~~~~.jpg
        created_at = data["created_at"] # 2021-02-28 00:00:00

        # ?? 헷갈림 
        user      = User.objects.get(email=user_email) # User클래스의 인스턴스

        Post.objects.create(user=user, created_at=created_at)

        post = Post.objects.get(user=user)

        Image.objects.create(image_url=image_url, post=post)

        return JsonResponse({"message": "SUCCESS"}, status=200)

        