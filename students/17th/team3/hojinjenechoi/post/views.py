import json
import my_settings
import datetime

from django.views                   import View
from django.http                    import JsonResponse

from user.models import User
from post.models import Post, Comment, Like

class PostView(View):
    def get(self, request):
        posts = Post.objects.all()
        result  = []

        for post in posts:
            result.append(
                {
                    'nickname'    : post.user.nickname,
                    'image'       : post.image,
                    'caption'     : post.caption,
                    'posted_time' : post.posted_time
                }
            )
        return JsonResponse({'message':'SUCCESS', 'data':result}, status=200)

    def post(self, request):
        try: 
            data = json.loads(request.body)

            image    = data['image']
            caption  = data.get('caption', None)
            nickname = data['nickname']

            if User.objects.filter(nickname=nickname).exists():
                Post.objects.create(
                    image    = image,
                    caption  = caption,
                    user     = User.objects.filter(nickname=nickname)[0]
                )
                return JsonResponse({'message':'SUCCESS'},status=200)

            return JsonResponse({'message':'INVALID_USER'},status=401)
    
        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class CommentsView(View):
    def get(self, request, post_id):
        comments = Post.objects.filter(post_id=post_id)
        result  = []

        for comment in comments:
            result.append(
                {
                    'nickname'    : comments.user.nickname,
                    'text'        : comments.text,
                    'posted_time' : comments.posted_time
                }
            )
        return JsonResponse({'message':'SUCCESS', 'data':result}, status=200)

    def post(self, request, post_id):
        try:
            data = json.loads(request.body)
            
            text     = data['text']
            nickname = data['nickname']

            if User.objects.filter(nickname=nickname).exists():
                Comment.objects.create(
                    text = text,
                    post = Post.objects.get(id=post_id),
                    user = User.objects.filter(nickname=nickname)[0]
                )
                return JsonResponse({'message':'SUCCESS'},status=200)

            return JsonResponse({'message':'INVALID_USER'},status=401)
    
        except KeyError: 
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class LikeView(View):
    def post(self, request, post_id):
        data = json.loads(request.body)

        nickname = data['nickname']
        post     = Post.objects.get(id=post_id)

        if not User.objects.filter(nickname=nickname).exists():
            return JsonResponse({'message':'USER_DOES_NOT_EXIST'},status=400)

        user = User.objects.get(nickname=nickname)

        if Like.objects.filter(post=post, user=user).exists():
            Like.objects.get(post=post, user=user).delete()

        like = Like.objects.create(post=post, user=user)
        return JsonResponse({'message':'SUCCESS'},status=200)

