import json
from django.views import View 
from .models import Users
from django.http import JsonResponse
from .models import Post_register, Post_express, Comments, Love
from user.utils import login_decorator
class Post(View):
    def get(self, request):
        all_post = Post_register.objects.all()
        post_list = []
        for post in all_post:
            post_list.append(
                {
                    'user_id' : post.id,
                    'content' : post.content,
                    'title' : post.title,
                    'image_url' : post.image_url,
                    'create_time' : post.create_time
                }
            )
        return JsonResponse({'message' : post_list}, status=200)
    
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user = Users.objects.get(email=data['user'])
        content = data['content']
        title = data['title']
        image_url = data['image_url']
        Post_register.objects.create(user = user, content = content, title = title, image_url = image_url)
        return JsonResponse({'message' : 'SUCCESS'}, status=200)



class Comment(View):
    @login_decorator        
    def post(self, request):
        data = json.loads(request.body)
        
        comment = data['comment']
        post = Post_register.objects.get(id=data["post_id"])
        user = Users.objects.get(email = data['user'])
        Comments.objects.create(post_register=post, user=user, comment=comment)
        return JsonResponse({"message" : "SUCCESS"}, status=200)


class Love_Function(View):  
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user = Users.objects.get(email = data['user'])
        post = Post_register.objects.get(id=data["post_id"])

        user_love = Love(
            user = user,
            post_register = post
              )
        user_love.save()
        return JsonResponse({"message" : "SUCCESS"}, status=200)
        

