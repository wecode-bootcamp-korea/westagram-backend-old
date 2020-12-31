import json
from decorator        import login_check
from django.shortcuts import render
from django.http      import JsonResponse
from django.views     import View
from .models          import Post, Image, Comment
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


    def get(self, request):
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


class CommentView(View):
    @login_check
    def post(self, request, post_id):
        try:
            data      = json.loads(request.body)
            post      = Post.objects.get(id=post_id)
            user      = User.objects.get(name=data['user'])
            pub_date  = datetime.now()
            content   = data['content']

            Comment(
                post      = post,
                user      = user,
                pub_date  = pub_date,
                content   = content
            ).save()

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
       
    
    def get(self, request, post_id): # post 출력 따로 comment 출력 따로..?
        post     = Post.objects.get(id=post_id)
        user     = post.user.name
        comments = post.comment_set.all()
        pub_date = post.pub_date

        if comments.count() == 0:
            return JsonResponse({'message':'댓글이 없는 포스트'}, status=400)

        contents_list = []
        for index, comment in enumerate(comments):
            contents_dict = {
                'content '+ str(index+1) : comment.content 
            }
            contents_list.append(contents_dict)

        comment_dict = {
            'post_id'  : post.id,
            'user'     : user,
            'contents' : contents_list,
            'pub_date' : pub_date 
        }

        return JsonResponse({'comment':comment_dict}, status=200)
       
        
