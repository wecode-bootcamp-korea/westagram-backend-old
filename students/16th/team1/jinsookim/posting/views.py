import json
import jwt

from django.views import View 
from django.http import JsonResponse

from westagram.settings import SECRET
from user.utils import login_decorator

from .models import Users
from .models import (Love,
                     Post_express,
                     Post_register, 
                     Comments_register,  
                     CommentsInComments)

class Post(View):
    def get(self, request):
        try:
            all_post = Post_register.objects.all()
            post_list = []
            for post in all_post:
                post_list.append(
                    {
                        'post_id'     : post.id,
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
        try:
            data      = json.loads(request.body)
        
            user      = request.user

            content   = data['content']
            title     = data['title']
            image_url = data['image_url']
            Post_register.objects.create(user = user, content = content, title = title, image_url = image_url)
        except KeyError :
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)
            
        return JsonResponse({'message' : 'SUCCESS'}, status=201)



class Comment(View):
    def get(self, request):
        try:
            all_comment = Comments_register.objects.all()

            if not all_comment.count():
                return JsonResponse({'message' : '댓글이 없습니다'}, status=400)

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
            return JsonResponse({'MESSAGE :':"KEY_ERROR"},status = 400)
     
        
            

    @login_decorator
    def post(self, request, post_id):
        try:
            data     = json.loads(request.body)
            comment  = data['comment']
            user     = request.user
            post     = Post_register.objects.get(id=post_id)

            if not comment:
                return JsonResponse({"message" : "댓글을 입력해주세요"}, status=400)

            Comments_register.objects.create(post_register=post, user=user, comment=comment)
            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except Post_register.DoesNotExist:
            return JsonResponse({"message" : "해당 게시물이 없습니다."}, status=400)

        except KeyError:
            return JsonResponse({"mesage" : "KeyError"}, status=400)


class Love_Function(View):  
    @login_decorator
    def post(self, request, post_id):
        try:
            user     = request.user
            post     = Post_register.objects.get(id=post_id)

            user_love = Love(
                user          = user,
                post_register = post
            )
            user_love.save()
            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except Post_register.DoesNotExist:
            return JsonResponse({"mesage" : "해당 게시물이 없습니다"}, status=400)




class Post_Delete_View(View):
    @login_decorator
    def post(self, request, post_id):
        try:
            user     = request.user

            if Post_register.objects.get(id = post_id):
                post = Post_register.objects.get(id = post_id)

                if user == post.user.id:
                    Post_register.objects.get(id = post_id).delete()

            return JsonResponse({"message" : "게시물이 정상적으로 삭제되었습니다."}, status=201)
            
        except Post_register.DoesNotExist:
            return JsonResponse({"message" : "해당 게시물이 없습니다."}, status=400)

        

class Comment_Delete_View(View):
    @login_decorator
    def post(self, request, post_id, comment_id):
        try:
            post    = Post_register.objects.get(id = post_id)
            comment = post.comments_register_set.get(id = comment_id)
            Comments_register.objects.filter(id = comment.id).delete()

            return JsonResponse({"message" : "SUCCESS"}, status = 201)

        except Post_register.DoesNotExist:
            return JsonResponse({"message" : "해당 게시물이 없습니다."}, status=400)
        
        except Comments_register.DoesNotExist:
            return JsonResponse({"message" : "해당 댓글이 없습니다."}, status=400)


class UpdateView(View):
    @login_decorator
    def post(self, request, post_id):
        try:
            data      = json.loads(request.body)

            content   = data.get("content")
            title     = data.get("title")
            image_url = data.get("image_url")

            if Post_register.objects.get(id=post_id):
                if content:
                    Post_register.objects.filter(id = post_id).update(content=content)
            
                if title:
                    Post_register.objects.filter(id = post_id).update(title=title)

                if image_url:
                    Post_register.objects.filter(id = post_id).update(image_url=image_url)

            return JsonResponse({"message" : "SUCCESS"}, status = 201)

        except Post_register.DoesNotExist:
            return JsonResponse({"message" : "해당 게시물이 없습니다."}, status=400)


class CommentsInCommentsView(View):
    @login_decorator
    def post(self, request, post_id, comment_id):
        try:
            data         = json.loads(request.body)

            user         = request.user
            content      = data["content"]
            post         = Post_register.objects.get(id = post_id) 
            comment      = Comments_register.objects.get(id = comment_id)
            post_comment = Comments_register.objects.filter(id = comment_id).select_related("post_register")
            print(comment)

            CommentsInComments.objects.create(user = user, comment = post_comment[0], content = content)

            return JsonResponse({"message" : "SUCCESS"}, status=200)
        except Post_register.DoesNotExist:
            return JsonResponse({"message" : "해당 게시물이 없습니다."}, status=400)

        except Comments_register.DoesNotExist:
            return JsonResponse({"message" : "해당 댓글이 없습니다."}, status=400)