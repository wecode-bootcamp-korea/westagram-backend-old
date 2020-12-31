import json
from decorator        import login_check
from django.shortcuts import render
from django.http      import JsonResponse
from django.views     import View
from .models          import Post, Image
from user.models      import User
from datetime         import datetime

# Create your views here.
class PostView(View):
    @login_check
    def post(self, request):
        try:
            data = json.loads(request.body)
            user     = User.objects.get(name=data['user'])
            image    = data['image']
            pub_date = datetime.now() # 2020-12-30 11:47:45.781887

            Post.objects.create(user=user, pub_date=pub_date)
            post = Post.objects.filter(user=user).last()
            Image.objects.create(post=post,image=image)

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


    def get(serlf, request):
        posts  = Post.objects.all()
        images = Image.objects.all()

        posts_list  = []
        images_list = []
        for post in posts:
            posts_dict = {
                'user'     : post.user.name,
                'pub_date' : post.pub_date
            }
        posts_list.append(posts_dict)

        for image in images:
            images_dict = {
                'image'  : image.image
            }
        posts_list.append(images_dict)

        return JsonResponse({'posts':posts_list}, status=200)



    

