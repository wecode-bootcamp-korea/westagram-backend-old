import json

from django.views import View
from django.http  import JsonResponse

from .models      import Post, Comment, Like
from user.models  import User
from utils        import login_decorator

class PostView(View):
    @login_decorator
    def post(self, request):
        data      = json.loads(request.body)
        user      = request.user
        image_url = data.get('image_url', None)
        content   = data.get('content', None)
        
        # KEY_ERROR check
        if not image_url:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
            
        post = Post.objects.create(
            user      = user,
            image_url = image_url,
            content   = content
        )

        return JsonResponse({'message': 'SUCCESS'}, status=200)

    def get(self, request):
        post_list = [{
                'user'      : post.user.name,
                'image_url' : post.image_url,
                'content'   : post.content,
                'created_at': post.created_at,
                'updated_at': post.updated_at,
            } for post in Post.objects.all()
        ]

        return JsonResponse({'data': post_list}, status=200)

class CommentView(View):
    @login_decorator
    def post(self, request):
        data    = json.loads(request.body)
        user    = request.user
        post_id = data.get('post', None)
        content = data.get('content', None)
        
        # KEY_ERROR check
        if not (post_id and content):
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        
        # valid post check
        if Post.objects.filter(id=post_id).exists():
            Comment.objects.create(
                user    = user,
                post    = Post.objects.get(id=post_id),
                content = content
            )
            return JsonResponse({'message': 'SUCCESS'}, status=200)

        return JsonResponse({'message': 'POST_DOES_NOT_EXISTS'}, status=400)

class PostDetailView(View):
    def get(self, request, post_id):
        # valid post check
        if not Post.objects.filter(id=post_id):
            return JsonResponse({'message': 'POST_DOES_NOT_EXISTS'}, status=404)
        
        context = {}

        # post 정보
        post = Post.objects.get(id=post_id)
        
        context['user']       = post.user.name
        context['image_url']  = post.image_url
        context['content']    = post.content
        context['created_at'] = post.created_at

        # comment 정보
        comments = Comment.objects.filter(post=post)
        if comments:
            comment_list = [{
                'user'      : comment.user.name,
                'content'   : comment.content,
                'created_at': comment.created_at
                } for comment in comments
            ]
            context['comment_list'] = comment_list

        return JsonResponse({'data': context}, status=200)

class LikeView(View):
    @login_decorator
    def post(self, request):
        data    = json.loads(request.body)
        user    = request.user
        post_id = data.get('post', None)

        # KEY_ERROR check
        if not post_id:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        # valid post check
        if Post.objects.filter(id=post_id).exists():
            post = Post.objects.get(id=post_id)

            # like 안 했을 때만 추가, 이미 했으면 삭제
            if post.liked_users.filter(id=user.id).exists():
                post.liked_users.remove(user)
                message = 'Cancle'
            else:
                post.liked_users.add(user)
                message = 'Like'

            like_count = post.liked_users.count()
            return JsonResponse({'message': message, 'like_count': like_count}, status=200)

        return JsonResponse({'message': 'POST_DOES_NOT_EXISTS'}, status=400)
