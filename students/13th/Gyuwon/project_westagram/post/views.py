import json
import re
import datetime

from django.db.models import Q
from django.views     import View
from django.http      import JsonResponse

from .models          import User
from .models          import Post, Comment, Like

class PostView(View):
    def post(self, request):
        try:
            data        = json.loads(request.body)
            name_id     = data['name_id']
            time        = datetime.datetime.now()
            image_url   = data['image_url']
            content     = data['content']

            Post.objects.create(
                name_id     = name_id,
                time        = time,
                image_url   = image_url,
                content     = content
            )

            return JsonResponse({'message' : 'Content Posted!'}, status=201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
            
    def get(self, request):
        data       = json.loads(request.body)
        posts      = Post.objects.values()

        return JsonResponse({'posts' : posts}, status=200)


class CommentView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            name_id         = data['name_id']
            time            = datetime.datetime.now()
            comment_content = data['comment_content']
            post_id         = data['post_id']

            Comment.objects.create(
                name_id         = name_id,
                time            = time,
                comment_content = comment_content,
                post_id         = post_id
            )

            return JsonResponse({'message' : 'Comment Posted!'}, status=201)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=200)

    def get(self, request):
        data = json.loads(request.body)
        comment = Comment.objects.filter(post_id = post_id).values()

        return JsonResponse ({'message' : 'Comments'}, status=200)


class LikeView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            name_id     = data['name_id']
            post_id     = data['post_id']

            if not Like.objects.filter(name_id = name_id, post_id = post_id).exists():
                Like.objects.create(
                    name_id = name_id,
                    post_id = post_id
                )
                return JsonResponse ({'message' : 'Liked!'}, stastus=201)
            else:
                return JsonResponse ({'message' : 'Already Liked!'}, status=409)
        except KeyError:
            return JsonResponse ({'message' : 'KEY_ERROR'}, status=400)
        

