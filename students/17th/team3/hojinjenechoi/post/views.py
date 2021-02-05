import json
import my_settings
import datetime

from django.views import View
from django.http  import JsonResponse

from user.models  import User
from post.models  import Post, Comment, Like
from user.utils   import login_decorator

class PostView(View):
    @login_decorator
    def get(self, request):
        posts = Post.objects.all()
        result  = []
        user = request.user

        for post in posts:
            result.append(
                {
                    'user'        : dict(user),
                    'image'       : post.image,
                    'caption'     : post.caption,
                    'posted_time' : post.posted_time
                }
            )
        return JsonResponse({'message':'SUCCESS', 'data':result}, status=200)

    @login_decorator
    def post(self, request):
        try: 
            data = json.loads(request.body)

            image    = data['image']
            caption  = data.get('caption', None)
            user     = request.user

            if User.objects.filter(email=user.email).exists():
                Post.objects.create(
                    image    = image,
                    caption  = caption,
                    user     = user
                )
                return JsonResponse({'message':'SUCCESS'},status=200)

            return JsonResponse({'message':'INVALID_USER'},status=401)
    
        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


class CommentsView(View):
    @login_decorator
    def get(self, request):
        data = json.loads(request.body)
        
        user     = request.user
        post_id  = data['post_id']
        comments = Post.objects.filter(post_id=post_id)
        result   = []

        for comment in comments:
            result.append(
                {
                    'user'        : user,
                    'text'        : comments.text,
                    'posted_time' : comments.posted_time
                }
            )
        return JsonResponse({'message':'SUCCESS', 'data':result}, status=200)

    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            user     = request.user
            text     = data['text']
            post_id  = data['post_id']
            
            if User.objects.filter(email=user.email).exists():
                Comment.objects.create(
                    text = text,
                    post = Post.objects.get(id=post_id),
                    user = user
                )
                return JsonResponse({'message':'SUCCESS'},status=200)

            return JsonResponse({'message':'INVALID_USER'},status=401)
    
        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


class LikeView(View):
    @login_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user    = request.user
            post    = Post.objects.get(id=data['post_id'])

            if Like.objects.filter(post=post, user=user).exists():
                Like.objects.get(post=post, user=user).delete()
                like_counts = Like.objects.filter(post=post).count()
                return JsonResponse({'message':'SUCCESS', 'like_counts':like_counts},status=200)

            like = Like.objects.create(post=post, user=user)
            like_counts = Like.objects.filter(post=post).count()
            return JsonResponse({'message':'SUCCESS', 'like_counts':like_counts},status=200)

        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

