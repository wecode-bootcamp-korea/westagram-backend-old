import json
import re

from django.views import View
from django.http  import JsonResponse

from user.models  import User
from .models      import Post, Comment
from utils        import login_decorator

class PostsView(View):
    @login_decorator
    def post(self, request):
        data      = json.loads(request.body)
        user_id   = request.user_id
        url_check = re.compile('https?://[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+/[a-zA-Z0-9-_.=?/]*')

        if not user_id or 'image_url' not in data or 'content' not in data: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        if not re.match(url_check, data['image_url']):
            return JsonResponse({'message':'BAD_IMAGE_URL_REQUEST'}, status=400)

        if len(data['content']) > 500:
            return JsonResponse({'message':'TOO_LONG_CONTENT'}, status=400)

        Post.objects.create(
            user_id   = user_id,
            content   = data['content'],
            image_url = data['image_url']
        )
        return JsonResponse({'message':'SUCCESS'}, status=200)
    
    def get(self, request):
        posts = Post.objects.select_related('user').prefetch_related('like_user')

        return JsonResponse(
        {
            'posts' : [
            {
                'name'       : post.user.name,
                'content'    : post.content,
                'image_url'  : post.image_url,
                'created_at' : post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'like'       : post.like_user.count()
            }
            for post in posts
        ]
    }, status=200) if posts else JsonResponse({'message':'NO_POST_DATA'}, status=404)

class PostDetailView(View):
    def get(self, request, post_id):
        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({'message':'POST_NOT_FOUND'}, status=404)

        post = Post.objects.prefetch_related('comment_set', 'like_user','comment_set__user').get(id=post_id)
        return JsonResponse(
        {
            'post' : {
                'name'       : post.user.name,
                'content'    : post.content,
                'image_url'  : post.image_url,
                'created_at' : post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'like'       : post.like_user.count(),
                'comments'   : [
                {
                    'name'       : comment.user.name,
                    'comment'    : comment.comment,
                    'created_at' : comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'parent_id'  : comment.parent_id 
                }
                for comment in post.comment_set.all()
            ] 
        }
    }, status=200)

    @login_decorator
    def put(self, request, post_id):
        data    = json.loads(request.body)
        user_id = request.user_id

        if not user_id:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        if 'image_url' not in data and 'content' not in data:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        if not Post.objects.filter(id=post_id, user_id=user_id).exists():
            return JsonResponse({'message':'POST_NOT_FOUND'}, status=404)

        post = Post.objects.get(id=post_id, user_id=user_id)

        if 'image_url' in data:
            post.image_url = data['image_url']

        if 'content' in data:
            post.content = data['content']
        post.save()
        return JsonResponse({'message':'SUCCESS'}, status=200)

    @login_decorator
    def delete(self, request, post_id):
        user_id = request.user_id

        if not user_id:
            return JsonResponse({'message':'INVALID_USER'},status=401)
        
        if not Post.objects.filter(id=post_id, user_id=user_id).exists():
            return JsonResponse({'message':'POST_NOT_FOUND'}, status=404)

        post = Post.objects.get(id=post_id, user_id=user_id)
        post.delete()
        return JsonResponse({'message':'SUCCESS'}, status=200)

class CommentView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user_id = request.user_id

        if not user_id:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        if 'comment' not in data or 'post_id' not in data: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        if len(data['comment']) > 100:
            return JsonResponse({'message':'TOO_LONG_COMMENT'}, status=400)

        if not Post.objects.filter(id=data['post_id']).exists():
            return JsonResponse({'message':'POST_NOT_FOUND'}, status=404)

        Comment.objects.create(
            user_id = user_id,
            post_id = data['post_id'],
            comment = data['comment']
        )
        return JsonResponse({'message':'SUCCESS'}, status=200)

    @login_decorator
    def put(self, request):
        data    = json.loads(request.body)
        user_id = request.user_id    

        if not user_id:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        
        if 'comment_id' not in data or 'comment' not in data:
            return JsonResponse({'message':'KEY_ERROR'}, status=400) 

        if len(data['comment']) > 100:
            return JsonResponse({'message':'TOO_LONG_COMMENT'}, status=400)
        
        if not User.objects.filter(id=user_id).exists():
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        if not Comment.objects.filter(id=data['comment_id'], user_id=user_id):
            return JsonResponse({'message':'COMMENT_NOT_FOUND'}, status=404)
        
        comment     = Comment.objects.get(
            id      = data['comment_id'],
            user_id = user_id,
        )
        comment.comment = data['comment']
        comment.save()
        return JsonResponse({'message':'SUCCESS'}, status=200)

    @login_decorator
    def delete(self, request):
        data    = json.loads(request.body)
        user_id = request.user_id

        if not user_id:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        if 'comment_id' not in data:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        if not Comment.objects.filter(id=data['comment_id'], user_id=user_id):
            return JsonResponse({'message':'COMMENT_NOT_FOUND'}, status=404)

        comment     = Comment.objects.get(
            id      = data['comment_id'],
            user_id = user_id
        )
        comment.delete()
        return JsonResponse({'message':'SUCCESS'}, status=200)

class CommentListView(View):
    def get(self, request, post_id):
        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({'message':'POST_NOT_FOUND'}, status=404)

        comments   = Comment.objects.filter(post_id=post_id).prefetch_related('user') 
        return JsonResponse(
        {
            'comments' : [
            {
                'name'       : comment.user.name,
                'comment'    : comment.comment,
                'created_at' : comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'parent_id'  : comment.parent_id
            }
            for comment in comments
        ]
    }, status=200) if comments else JsonResponse({'message':'None_comment_data'}, status=200)

class LikeView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user_id = request.user_id

        if not user_id:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        if 'post_id' not in data:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        if not Post.objects.filter(id=data['post_id']).exists():
            return JsonResponse({'message':'POST_NOT_FOUND'}, status=404)
        
        user_model = User.objects.get(id=user_id)
        post_model = Post.objects.get(id=data['post_id'])
        user_model.like.add(post_model)
        return JsonResponse({'message':'SUCCESS'}, status=200)
    
    @login_decorator
    def delete(self, request):
        data    = json.loads(request.body)
        user_id = request.user_id

        if not user_id:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        
        if 'post_id' not in data:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        if not Post.objects.filter(id=data['post_id']).exists():
            return JsonResponse({'message':'POST_NOT_FOUND'}, status=404)

        user_model = User.objects.get(id=user_id)
        post_model = Post.objects.get(id=data['post_id'])
        user_model.like.remove(post_model)
        return JsonResponse({'message':'SUCCESS'}, status=200)

class LikeListView(View):
    def get(self, request, user_id):
        if not User.objects.filter(id=user_id).exists():
            return JsonResponse({'message':'USER_NOT_EXIST'}, status=404)

        like_posts = User.objects.get(id=user_id).like.prefetch_related('like_user', 'user')
        return JsonResponse(
        {
            'posts' : [
            {
                'name'       : like_post.user.name,
                'content'    : like_post.content,
                'image_url'  : like_post.image_url,
                'created_at' : like_post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'like'       : like_post.like_user.count()
            }
            for like_post in like_posts
        ]
    }, status=200) if like_posts else JsonResponse({'message':'NO_LIKE_DATA'}, status=404)

class ReplyToCommentsView(View):
    @login_decorator
    def post(self, request, comment_id):
        data    = json.loads(request.body)
        user_id = request.user_id

        if not user_id:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        if 'reply' not in data:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        if len(data['reply']) > 100:
            return JsonResponse({'message':'TOO_LONG_REPLY'}, status=400)

        if not Comment.objects.filter(id=comment_id).exists():
            return JsonResponse({'message':'COMMENT_NOT_FOUND'}, status=404)

        comment_model  = Comment.objects.get(id=comment_id)
        Comment.objects.create(
            user_id    = user_id,
            comment    = data['reply'],
            post_id    = comment_model.post.id,
            parent_id  = comment_model.id
        )
        return JsonResponse({'message':'SUCCESS'}, status=200)

    @login_decorator
    def put(self, request, comment_id):
        data    = json.loads(request.body)
        user_id = request.user_id

        if not user_id:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        
        if 'reply' not in data or 'reply_id' not in data:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        if len(data['reply']) > 100:
            return JsonResponse({'message':'TOO_LONG_REPLY'}, status=400)
        
        if not Comment.objects.filter(id=data['reply_id'], parent_id=comment_id, user_id=user_id).exists():
            return JsonResponse({'message':'REPLY_NOT_FOUND'}, status=404)

        reply_model   = Comment.objects.get(
            id        = data['reply_id'],
            parent_id = comment_id, 
            user_id   = user_id
        )
        reply_model.comment = data['reply']
        reply_model.save()
        return JsonResponse({'message':'SUCCESS'}, status=200)

    @login_decorator
    def delete(self, request, comment_id):
        data    = json.loads(request.body)
        user_id = request.user_id
    
        if not user_id:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
        
        if 'reply_id' not in data:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        if not Comment.objects.filter(id=data['reply_id'], user_id=user_id, parent_id=comment_id).exists():
            return JsonResponse({'message':'REPLY_NOT_FOUND'}, status=404)

        reply_model   = Comment.objects.get(
            id        = data['reply_id'],
            user_id   = user_id,
            parent_id = comment_id
        ) 
        reply_model.delete()
        return JsonResponse({'message':'SUCCESS'}, status=200)
