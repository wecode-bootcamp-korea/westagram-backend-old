import json

from django.views import View
from django.http  import JsonResponse

from post.models  import Post
from user.models  import User

class PostView(View):
    def post(self, request):
        data          = json.loads(request.body)
        user_name     = data.get('user')
        image         = data.get('image')
        user_obj      = User.objects.get(name= user_name)
        print(user_obj, image)
        Post.objects.create(user= user_obj, image= image)
        
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

    def get(self, request):
        data         = json.loads(request.body)
        user_name    = data.get('user')
        user_obj     = User.objects.get(name= user_name)
        posts        = Post.objects.filter(user= user_obj)
        post_lst     =[]

        for post in posts:
            post_lst.append((post.user, post.post_time, post.image))
            
        return JsonResponse({'IMAGES':post_lst}, status=200)