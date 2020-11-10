import json
import re

from django.views import View
from django.http import JsonResponse

from user.models import User
from .models import Post, Comment

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
            Post.objects.create( user_id   = user_model.id,
                content   = data['content'],
                image_url = data['image_url']
            )
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
    
    def get(self, request):
        posts = Post.objects.prefetch_related('user')

        return JsonResponse({
            'posts' : [{
                'name'       : post.user.name,
                'content'    : post.content,
                'image_url'  : post.image_url,
                'created_at' : post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'like'       : post.like_user.count()
            } for post in posts]}, status=200) if posts else JsonResponse({'message':'None_post_data'}, status=200)

class PostDetailView(View):
    def get(self, request, post_id):
        try:
            post_model = Post.objects.get(id=post_id)
            comments = Comment.objects.filter(post_id=post_id).prefetch_related('user') 
            posts = Post.objects.prefetch_related('comment_set')
            return JsonResponse({
                'post' : [{
                    'name'       : post.user.name,
                    'content'    : post.content,
                    'image_url'  : post.image_url,
                    'created_at' : post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'like'       : post.like_user.count(),
                    'comments'   : [{
                        'name'       : comment.user.name,
                        'comment'    : comment.comment,
                        'created_at' : comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                        'parent_id'  : comment.parent_id if comment.parent_id else None 
                    } for comment in comments] if comments else '' 
                } for post in posts]
            }, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'message':'POST_NOT_FOUND'}, status=404)

    def put(self, request, post_id):
        data = json.loads(request.body)

        if 'user_id' not in data:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        if (len(data) > 3) or ('image_url' not in data and 'content' not in data and len(data) > 1):
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        try:
            post = Post.objects.get(id=post_id, user_id=data['user_id'])
            if 'image_url' in data:
                post.image_url = data['image_url']
            if 'content' in data:
                post.content = data['content']
            post.save()
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except Post.DoesNotExist:
            return JsonResponse({'message':'POST_NOT_FOUND'}, status=404)

    def delete(self, request, post_id):
        data = json.loads(request.body)

        if 'user_id' not in data:
            return JsonResponse({'message':'INVALID_USER'},status=401)

        if len(data) >= 2:
            return JsonResponse({'message':'KEY_ERROR'},status=400)
        try:
            post = Post.objects.get(id=post_id, user_id=data['user_id'])
            post.delete()
            return JsonResponse({'message':'SUCCESS'}, status=204)
        except Post.DoesNotExist:
            return JsonResponse({'message':'POST_NOT_FOUND'}, status=404)

class CommentView(View):
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

    def put(self, request):
        data = json.loads(request.body)

        if 'user_id' not in data:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        
        if 'comment_id' not in data or 'comment' not in data or len(data) != 3:
            return JsonResponse({'message':'KEY_ERROR'}, status=400) 

        if len(data['comment']) > 100:
            return JsonResponse({'message':'TOO_LONG_COMMENT'}, status=400)

        try:
            user_model = User.objects.get(id=data['user_id'])
            comment    = Comment.objects.get(
                id      = data['comment_id'],
                user_id = user_model.id,
        )
            comment.comment = data['comment']
            comment.save()
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        except Comment.DoesNotExist:
            return JsonResponse({'message':'COMMENT_NOT_FOUND'}, status=404)

    def delete(self, request):
        data = json.loads(request.body)

        if 'user_id' not in data:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        if 'comment_id' not in data or len(data) > 2:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        try:
            user_model = User.objects.get(id=data['user_id'])
            comment    = Comment.objects.get(
                id      = data['comment_id'],
                user_id = user_model.id
        )
            comment.delete()
            return JsonResponse({'message':'SUCCESS'}, status=204)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        except Comment.DoesNotExist:
            return JsonResponse({'message':'COMMENT_NOT_FOUND'}, status=404)

class CommentListView(View):
    def get(self, request, post_id):
        if not post_id:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        try:
            post_model = Post.objects.get(id=post_id)
            comments   = Comment.objects.filter(post_id=post_id).prefetch_related('user') 
            return JsonResponse({
                'comments' : [{
                    'name'       : comment.user.name,
                    'comment'    : comment.comment,
                    'created_at' : comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'parent_id'  : comment.parent_id if comment.parent_id else None
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
            user_model.like.add(post_model)
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        except Post.DoesNotExist:
            return JsonResponse({'message':'POST_NOT_FOUND'}, status=404)
    
class LikeListView(View):
    def get(self, request, user_id):
        try:
            user_model      = User.objects.get(id=user_id)
            like_posts      = user_model.like.prefetch_related('like_user')
            return JsonResponse({
                'posts' : [{
                    'name'       : like_post.user.name,
                    'content'    : like_post.content,
                    'image_url'  : like_post.image_url,
                    'created_at' : like_post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'like'       : like_post.like_user.count() 
                } for like_post in like_posts]}, status=200) if like_posts else JsonResponse({'message':'None_like_data'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

class ReplyToCommentsView(View):
    def post(self, request, comment_id):
        data = json.loads(request.body)

        if 'user_id' not in data:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        if 'reply' not in data or len(data) > 2:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        if len(data['reply']) > 100:
            return JsonResponse({'message':'TOO_LONG_REPLY'}, status=400)

        try:
            user_model    = User.objects.get(id=data['user_id'])
            comment_model = Comment.objects.get(id=comment_id)
            Comment.objects.create(
                user_id    = data['user_id'],
                comment    = data['reply'],
                post_id    = comment_model.post.id,
                parent_id  = comment_model.id
            )
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        except Comment.DoesNotExist:
            return JsonResponse({'message':'COMMENT_NOT_FOUND'}, status=404)

    def put(self, request, comment_id):
        data = json.loads(request.body)

        if 'user_id' not in data:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        
        if 'reply' not in data or 'reply_id' not in data or len(data) > 3:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        if len(data['reply']) > 100:
            return JsonResponse({'message':'TOO_LONG_REPLY'}, status=400)

        try:
            user_model   = User.objects.get(id=data['user_id'])
            reply_model  = Comment.objects.get(
                id        = data['reply_id'],
                parent_id = comment_id, 
                user_id   = data['user_id']
            )
            reply_model.comment = data['reply']
            reply_model.save()
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        except Comment.DoesNotExist:
            return JsonResponse({'message':'REPLY_NOT_FOUND'}, status=404)

    def delete(self, request, comment_id):
        data = json.loads(request.body)

        if 'user_id' not in data:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        
        if 'reply_id' not in data or len(data) > 2:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        try:
            user_model  = User.objects.get(id=data['user_id'])
            reply_model = Comment.objects.get(
                id        = data['reply_id'],
                user_id   = user_model.id,
                parent_id = comment_id
            ) 
            reply_model.delete()
            return JsonResponse({'message':'SUCCESS'}, status=204)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        except Comment.DoesNotExist:
            return JsonResponse({'message':'REPLY_NOT_FOUND'}, status=404)


