import json
import post
from my_settings import DATABASES

from django.views import View
from django.http  import JsonResponse

from post.models  import Post, Comment
from user.models  import User

class PostView(View):
    def post(self, request):
        data          = json.loads(request.body)
        user_name     = data.get('user')
        image         = data.get('image')
        user          = User.objects.filter(name= user_name)

        if user.exists():
            Post.objects.create(image= image, user= user[0])

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)

    def get(self, request):
        posts        = Post.objects.all()
        post_data    = [
            {
                "post_id" : post.id,
                "image" : post.image,
                "post_time" : post.post_time
            }
            for post in posts
        ] 

        return JsonResponse({'post_data':post_data}, status=200)

class CommentCreateView(View):
    def post(self, request, post_id):
        data            = json.loads(request.body)
        post_id         = post_id
        user_name       = data.get('user')
        comments        = data.get('comments')
        user            = User.objects.filter(name= user_name)
        post            = Post.objects.get(id= post_id)

        if user.exists():
            Comment.objects.create(user= user[0], post=post, comment= comments)
            
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=400)
        
   
    def get(self, request, post_id):
        post_id         = post_id
        post            = Post.objects.get(id=post_id)
        comments        = Comment.objects.filter(post=post)
        comments_data   = [
            {
                'comment'       : comment.comment,
                'user'          : comment.user.name,
                'comment_time'  : comment.comment_time
            }
            for comment in comments
        ]

        return JsonResponse({'comments': comments_data}, status=200)