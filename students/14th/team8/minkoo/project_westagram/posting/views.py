import json
import re

from django.views import View
from django.http import JsonResponse

from user.models import User
from .models import Post, Comment, Like

class PostsView(View):
    def post(self, request):
        data = json.loads(request.body)
        url_check = re.compile('https?://[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+/[a-zA-Z0-9-_.=?/]*')

        if 'image_url' not in data or 'user_id' not in data or 'content' not in data  or len(data) != 3:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        if not re.match(url_check, data['image_url']):
            return JsonResponse({'message':'BAD_IMAGE_URL_REQUEST'}, status=400)
        if len(data['content']) > 500:
            return JsonResponse({'message':'TOO_LONG_CONTENT'}, status=400)

        try:
            user_model = User.objects.get(id=data['user_id'])
            Post.objects.create(
                user_id   = user_model.id,
                content   = data['content'],
                image_url = data['image_url']
            )
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
    
    def get(self, request):
        posts = Post.objects.all()
        return JsonResponse({
            'posts' : [{
                'name' : post.user.name,
                'content'    : post.content,
                'image_url'  : post.image_url,
                'created_at' : post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'like'       : len(post.like_set.all())
            } for post in posts]}, status=200) if posts else JsonResponse({'message':'None_post_data'}, status=200)

class CommentCreateView(View):
    def post(self, request):
        data = json.loads(request.body)

        if 'comment' not in data or 'post_id' not in data or 'user_id' not in data or len(data) != 3:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        if len(data['comment']) > 100:
            return JsonResponse({'message':'TOO_LONG_COMMENT'}, status=400)

        try:
            user_model = User.objects.get(id=data['user_id'])
            post_model = Post.objects.get(id=data['post_id'])
            Comment.objects.create(
                user_id = user_model.id,
                post_id = post_model.id,
                comment = data['comment']
            )
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        except Post.DoesNotExist:
            return JsonResponse({'message':'POST_NOT_FOUND'}, status=404)

class CommentListView(View):
    def get(self, request, post_id):
        if not post_id:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        try:
            post_model = Post.objects.get(id=post_id)
            comments = Comment.objects.filter(post_id=post_id) 
            return JsonResponse({
                'comments' : [{
                    'name'       : comment.user.name,
                    'comment'    : comment.comment,
                    'created_at' : comment.created_at.strftime('%Y-%m-%d %H : %M : %S')
                } for comment in comments]}, status=200) if comments else JsonResponse({'message':'None_comment_data'}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'message':'POST_NOT_FOUND'}, status=404)

class LikeView(View):
    def post(self, request):
        data = json.loads(request.body)

        if 'user_id' not in data or 'post_id' not in data or len(data) != 2:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        try:
            post_model = Post.objects.get(id=data['post_id'])
            user_model = User.objects.get(id=data['user_id'])
            Like.objects.create(
                user_id = data['user_id'],
                post_id = data['post_id']
            )
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        except Post.DoesNotExist:
            return JsonResponse({'message':'POST_NOT_FOUND'}, status=404)
    
class LikeListView(View):
    def get(self, request, user_id):
        if not user_id:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        try:
            user_model = User.objects.get(id=user_id)
            likes = Like.objects.filter(user_id=user_id)
            return JsonResponse({
                'posts' : [{
                    'name'       : like.post.user.name,
                    'content'    : like.post.content,
                    'image_url'  : like.post.image_url,
                    'created_at' : like.post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'like'       : len(like.post.like_set.all())
                } for like in likes]}, status=200) if likes else JsonResponse({'message':'None_like_data'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
