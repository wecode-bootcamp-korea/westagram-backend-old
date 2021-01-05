import json
import jwt
from django.views import View 
from westagram.settings import SECRET
from .models import Users
from django.http import JsonResponse
from .models import Post_register, Post_express, Comments_register, Love
from user.utils import login_decorator

class Post(View):
    def get(self, request):
        try:
            all_post = Post_register.objects.all()
            post_list = []
            for post in all_post:
                post_list.append(
                    {
                        'user_id'     : post.id,
                        'content'     : post.content,
                        'title'       : post.title,
                        'image_url'   : post.image_url,
                        'create_time' : post.create_time,
                        'update_time' : post.update_time
                    }
                )
            return JsonResponse({'message' : post_list}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)

            
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        token     = request.headers.get('Token')
        access    = jwt.decode(token, SECRET, algorithms="HS256").get("id")
        user      = Users.objects.get(id = access)
        content   = data['content']
        title     = data['title']
        image_url = data['image_url']
        Post_register.objects.create(user = user, content = content, title = title, image_url = image_url)
        return JsonResponse({'message' : 'SUCCESS'}, status=200)



class Comment(View):
    def get(self, request):
        try:
            all_comment = Comments_register.objects.all()

            if not all_comment.count():
                return JsonResponse({'message' : '댓글이 없습니다'}, status=200)

            comment_list = []
            for comment in all_comment:
                comment_dic = {
                    'id'          : comment.id,
                    'comment'     : comment.comment,
                    'user'        : comment.user.user_name,
                    'post'        : comment.post_register.id,
                    'create_time' : comment.create_time,
                    'update_time' : comment.update_time
                }
                comment_list.append(comment_dic)
            return JsonResponse({'message' : comment_list}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 40)
     
        
            

    @login_decorator
    def post(self, request):
        data    = json.loads(request.body)
        comment = data['comment']
        post    = Post_register.objects.get(id=data["post_id"])
        user    = Users.objects.get(email = data['user'])
        Comments_register.objects.create(post_register=post, user=user, comment=comment)
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



        

