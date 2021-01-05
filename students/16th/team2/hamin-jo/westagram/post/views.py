import json
from typing import ContextManager

from django.views import View
from django.http  import JsonResponse

from post.models  import Post
from user.models  import User

class PostView(View):
    def post(self, request):
        data          = json.loads(request.body)
        user_name     = data.get('user')
        user      = User.objects.filter(name= user_name)
        image         = data.get('image')

        if user.exists():
            Post.objects.create(image= image, user= user[0])
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)


    def get(self, request):
        posts        = Post.objects.all()
        post_data    = [
            {
                "user_id" : post.id,
                "image" : post.image,
                "post_time" : post.post_time
            }
            for post in posts
        ] 

        return JsonResponse({'post data':post_data}, status=200)

class CommentView(View):
    def post(self,request):
        data         = json.loads(request.body)
        user_name    = data.get('user')
        user_obj     = User.objects.get(name= user_name)
