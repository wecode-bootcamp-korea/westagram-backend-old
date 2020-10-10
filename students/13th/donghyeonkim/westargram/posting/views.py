import re
import json

from django.db.models import Q
from django.http      import JsonResponse
from django.views     import View

from user.models      import User
from posting.models   import Post

class CreatePost(View):
    def post(self, request):
        post_info       = json.loads(request.body)
        user_id         = post_info['user_id']
        image_url       = post_info['image_url']
        posting_comment = post_info['posting_comment']
        
        Post.objects.create(
            user_id         = user_id,
            image_url       = image_url,
            posting_comment = posting_comment)

        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

class PostView(View):
    def get(self, request):
        post_info = json.loads(request.body)
        user_id   = post_info['user_id']

        view = []
        posts = Post.objects.filter(user_id=user_id).values_list()
        user_name = User.objects.get(id=user_id).name

        for post in posts:
            image_url       = post[2]
            posting_comment = post[3]
            time            = post[1]
            view.append([
                user_name,
                image_url,
                posting_comment,
                time
                ])
        return JsonResponse({'MESSAGE':view}, status=200)