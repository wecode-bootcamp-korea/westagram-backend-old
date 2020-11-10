import json

from django.shortcuts import render
from django.views     import View
from django.http      import JsonResponse
from django.db.models import Sum

from .models     import Post, Comment
from user.models import User
from core.utils  import login_decorator

class PostView(View):
    def get(self, request, *args, **kwargs):
        try:
            posts = Post.objects.select_related('author')
            comments = Comment.objects.prefetch_related('post_id')
            context = [
                {
                    'id'      : post.id,
                    'author'  : post.author.username,
                    'title'   : post.title,
                    'image'   : post.image,
                    'created' : post.post_created,
                    'likes'   : Likes.objects.filter(id=post.id).count(),
                    'comment' : [
                        {
                            'parent': cmt.parent_id,
                            'created': cmt.comment_created,
                            'content': cmt.content,
                            'id': cmt.id
                        }
                        for cmt in comments
                    ]
                }
                for post in posts
            ]
            return JsonResponse({'result':context}, status =200)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            if 'content' in data:
                Post.objects.create(
                    author  = User.objects.get(id = data['user_id']),
                    title   = data['title'],
                    content = data['content'],
                    image   = data['image'])
                return JsonResponse({'message': 'POST HAS BEEN CREATED SUCCESSFULLY!'}, status = 201)
            Post.objects.create(author = User.objects.get(id=data['id']), title = data['title'], image = data['image'])
            return JsonResponse({'message': 'Post has been created successfully!'}, status = 201)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

    @login_decorator
    def put(self, request):
        try:
            data = json.loads(request.body)
            obj = Post.objects.get(id=data['id'])
            if 'title' in data:
                obj.title = data['title']
            if 'content' in data:
                obj.content = data['content']
            if 'image' in data:
                obj.image = data['image']
            obj.save()
            return JsonResponse({'message': 'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)

    @login_decorator
    def delete(self, request):
        try:
            data = json.loads(request.body)
            if Post.objects.filter(id = data['id']).exists():
               q = Post.objects.get(id = data['id'])
               q.delete()
               return JsonResponse({'message': 'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status = 400)


class CommentView(View):

    def get(self, request):
        try:
            data = json.loads(request.body)
            if 'post_id' in data:
                qs = Comment.objects.filter(post_id = data['post_id']).prefetch_related('author')
                context = [
                    {
                    'feed_id'      : cmt.post_id.id,
                    'author'       : cmt.author.username,
                    'content'      : cmt.content,
                    'created_time' : cmt.comment_created,
                    'parent'       : cmt.parent_idi
                    }
                    for cmt in qs
                ]

                return JsonResponse({'result':context}, status = 200)
        except KeyError:
            JsonResponse({'message':'nope'}, status = 400)

    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            if 'parent_id' in data:
                Comment.objects.create(
                    author          = User.objects.get(id = data['user_id']),
                    post_id         = Post.objects.get(id = data['post_id']),
                    content         = data['content'],
                    parent          = Comment.objects.get(id = data['parent_id']))
            Comment.objects.create(
                author = User.objects.get(id=data['user_id']),
                post_id=Post.objects.get(id=data['post_id']),
                content=data['content'])
            return JsonResponse({'meesage':'SUCCESS'}, status = 200)
        except KeyError:
            JsonResponse({'message':'KEY_ERROR'}, status = 400)

    @login_decorator
    def put(self, request):
        try:
            data = json.loads(request.body)
            if Comment.objects.filter(id=data['id']).exists():
                q = Comment.objects.get(id=data['id'])
                q.content = data['content']
                q.save()
                return JsonResponse({'message':'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'meesage':'KEY_ERROR'}, status = 400)

    @login_decorator
    def delete(self, request):
        try:
            data = json.loads(request.body)
            if Comment.objects.filter(id=data['id']).exists():
                q = Comment.objects.get(id=data['id'])
                q.delete()
                return JsonResponse({'message':'cmt, success'}, status = 200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 200)

class LikeView(View):

    def post(self, request):
        try:
            data=json.loads(request.body)
            Like.objects.create(user_id = data['user_id'], post_id = data['post_id'])
            return JsonResponse({'message':'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

class FollowView(View):
    def post(self, request):
        try:
            data=json.loads(request.body)
            Like.objects.create(user_id = data['user_id'], post_id = data['post_id'])
            return JsonResponse({'message':'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)



