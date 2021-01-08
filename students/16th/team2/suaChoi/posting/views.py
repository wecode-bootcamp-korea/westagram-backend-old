import json
import re

from django.http  import JsonResponse
from django.views import View

from .models     import Post
from user.models import User
from user.utils  import check_user

class PostView(View):

    def post(self, request):

        try:
            data      = json.loads(request.body)
            email     = data['email']
            image_url = data['image_url']
            content   = data.get('content')

            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                Post.objects.create(user=user, image_url=image_url, content=content)
                return JsonResponse({"message": "SUCCESS"}, status=200)
            return JsonResponse({"message":"INVALID_USER"}, status=401)

        except:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    def get(self, request):
        posts = Post.objects.all()
        post_list = []
        for post in posts:
            post_list.append({
                'user_id'    : post.id,
                'content'    : post.content,
                'image_url'  : post.image_url,
                'created_at' : post.created_at
            })
        return JsonResponse({"posts": post_list}, status=200)

class CommentView(View):

    @check_user
    def post(self, request):

        try:
            data = json.loads(request.body)
            Comment = Post.objects.get(
                writer = request.user,
                reply  = data['reply']
            )
            return JsonResponse({"message": "SUCCESS"}, status=200)

        except:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
