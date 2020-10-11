import re
import json

from django.db.models import Q
from django.http      import JsonResponse
from django.views     import View

from user.models      import User
from posting.models   import Post

class LikeView(View):
    def get(self, request, post_id):
        post = Post.objects.get(id=post_id)
        like_count = post.likes.all().count()
        return JsonResponse({'Like count':like_count}, status=200)

    def post(self, request, post_id):
        data = json.loads(request.body)
        user = data['user_id']

        post = Post.objects.get(pk=post_id)   
        user = User.objects.get(id=user)
        if user in post.likes.all():
            post.likes.remove(user)
            return JsonResponse({'MESSAGE':'좋아요를 취소했습니다.'}, status=200)
        post.likes.add(user)
        return JsonResponse({"MESSAGE":"좋아요를 눌렀습니다."}, status=200)





