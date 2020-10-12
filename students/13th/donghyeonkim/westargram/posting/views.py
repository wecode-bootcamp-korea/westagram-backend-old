import re
import json

from django.db.models import Q
from django.http      import JsonResponse
from django.shortcuts import get_object_or_404
from django.views     import View

from user.models      import User
from posting.models   import Post, Comment

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
    def get(self, request, user_id):
        posts_view      = []
        posts     = Post.objects.all().values_list()
        user_name = User.objects.get(id=user_id).name

        for post in posts:
            user_name       = User.objects.get(id=post[4]).name
            image_url       = post[2]
            posting_comment = post[3]
            time            = post[1]
            posts_view.append([
                user_name,
                image_url,
                posting_comment,
                time
            ])
        return JsonResponse({'MESSAGE':posts_view}, status=200)
    
    def delete(self, request, user_id):
        post_info = json.loads(request.body)
        post_id   = post_info['post_id']

        try:
            post = Post.objects.get(pk=post_id)
            post.delete()
            return JsonResponse({'MESSAGE':"게시물을 삭제하였습니다."}, status=400)
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':"게시물이 존재하지 않습니다."}, status=400)
            

class CreateComment(View):
    def post(self, request, post_id):
        comment_info = json.loads(request.body)
        user_id      = comment_info['user_id']
        comment      = comment_info['comment']
        
        Comment.objects.create(
            user_id = user_id,
            post_id = post_id,
            comment = comment
            )

        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

class CommentView(View):
    def get(self, request, post_id):
        comment_view = []
        comments     = Comment.objects.filter(post_id=post_id).values_list()

        for comment in comments:
            user_name    = User.objects.get(id=comment[3]).name
            comment_text = comment[1]
            time         = comment[2]
            comment_view.append([
                user_name,
                comment_text,
                time
            ])
        return JsonResponse({'MESSAGE':comment_view}, status=200)
    
    def delete(self, request, post_id):
        comment_info = json.loads(request.body)
        comment_id   = comment_info['comment_id']

        try:
            comment = Comment.objects.get(pk=comment_id)
            comment.delete()
            return JsonResponse({'MESSAGE':"댓글을 삭제하였습니다."}, status=200)
        except Comment.DoesNotExist:
            return JsonResponse({'MESSAGE':"댓글이 존재하지 않습니다."}, status=400)
