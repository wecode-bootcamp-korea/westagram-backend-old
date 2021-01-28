import json
import post
from my_settings import DATABASES

from django.views import View
from django.http  import JsonResponse

from post.models  import Post, Comment
from user.models  import User
from core.util    import login_decorator

#@login_decorator
class PostView(View):
    def post(self, request):
        try:
            data          = json.loads(request.body)
            email         = data['email']
            image         = data['image']
            user          = User.objects.filter(email= email)
            print(request.user)
            if not user.exists():
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)       

            if image is None:
                return JsonResponse({'MESSAGE': 'NO_IMAGE'}, status=401)

            Post.objects.create(image= image, user= user)
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

        except:
            return JsonResponse({'MESSAGE': 'KEYERROR'}, status=401)  



    def get(self, request):
        posts        = Post.objects.all()
        post_data    = [
            {
                "post_id"   : post.id,
                "image"     : post.image,
                "post_time" : post.post_time
            }
            for post in posts
        ] 

        return JsonResponse({'post_data':post_data}, status=200)

class CommentCreateView(View):
    def post(self, request, post_id):
        try:
            data            = json.loads(request.body)
            post_id         = post_id
            comments        = data['comments']
            user            = User.objects.filter(name= data['email'])
            post            = Post.objects.get(id= post_id)

            if user.exists():
                Comment.objects.create(user= user, post=post, comment= comments)
                
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

            else:
                return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=400)

        except:
            return JsonResponse({'MESSAGE': 'KEYERROR'}, status=401)  

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