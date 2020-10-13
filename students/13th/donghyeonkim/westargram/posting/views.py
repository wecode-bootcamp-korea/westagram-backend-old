import re
import json

from django.db.models import Q
from django.http      import JsonResponse
from django.shortcuts import get_object_or_404
from django.views     import View
from django.utils     import timezone

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

        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

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
            return JsonResponse({'MESSAGE':"게시물을 삭제하였습니다."}, status=204)
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':"게시물이 존재하지 않습니다."}, status=404)
            
    def put(self, request, user_id):
        post_info       = json.loads(request.body)
        post_id         = post_info['post_id']
        image_url       = post_info['image_url']
        posting_comment = post_info['posting_comment']
        
        try:
            post = Post.objects.filter(pk=post_id)
            post.update(
                user_id         = user_id,
                image_url       = image_url,
                posting_comment = posting_comment,
                time            = timezone.now()
            )
            return JsonResponse({'MESSAGE':"게시물을 수정하였습니다."}, status=204)
        except Post.DoesNotExist:
            return JsonResponse({'MESSAGE':"게시물이 존재하지 않습니다."}, status=404)

class CreateComment(View):
    def post(self, request):
        comment_info = json.loads(request.body)
        user_id      = comment_info['user_id']
        comment      = comment_info['comment']
        post_id      = comment_info['post_id']

        try:
            response_to = comment_info['response_to']
        except KeyError:
            response_to = None
        Comment.objects.create(
            user_id     = user_id,
            post_id     = post_id,
            comment     = comment,
            response_to = response_to
            )
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)

class CommentView(View):
    def post(self, request, post_id, user_id):
    
        try:
            comment_info = json.loads(request.body)
            response_to = comment_info['response_to']
        except ValueError:
            response_to = None

        comments = Comment.objects.filter(response_to=response_to).values(
            'user__name',
            'comment',
            'time'
        )
    
        return JsonResponse({'MESSAGE':list(comments)}, status=200)
    
    def put(self, request, post_id, user_id):
        comment_info = json.loads(request.body)
        comment_id   = comment_info['comment_id']

        comment = Comment.objects.filter(pk=comment_id)
        if comment:
            comment.update(
                comment = "삭제된 댓글입니다.",
                time    = timezone.now()  
                )
            return JsonResponse({'MESSAGE':"댓글을 삭제하였습니다."}, status=204)
        return JsonResponse({'MESSAGE':"댓글이 존재하지 않습니다."}, status=404)
