import json

from django.views           import View
from django.http            import JsonResponse
from django.db              import models

from user.models            import User
from .models                import Post, Comment

class PostView(View):
    # 먼저 게시물을 등록하려는 유저의 정보를 받아들인다.
    # 해당 게시물의 유저는 Foreign Key를 이용하여
    # 서비스에 가입된 사람으로 연결

    def post(self, request):
        data = json.loads(request.body)
        try:
            post = Post (
                content    = data['content'],
                image_url  = data['image_url']
            )
            post.user = User.objects.get(email = data['email'])

        except User.DoesNotExist:
            return JsonResponse({"message": "can't be found email"})

        except KeyError:
            return JsonResponse({"messsage": "KEY_ERROR"}, status = 400)

        post.save()
        return JsonResponse({"message": "SUCCESS"}, status = 200)

class PostGet(View):
    def get(self, request):
        post = Post.objects.values()
        return JsonResponse({"message": list(post)}, status = 200)

# url('posting/post_comment')
class CommentPost(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user_email = data['email']
            user_content = data['content']
            comment_post = Post.objects.get(id = 1)
            comment_user = User.objects.get(email = data['email'])
        except ValueError:
            return JsonResponse({"message": "VALUE_ERROR"}, status = 400)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        Comment(
                email   = data['email'],
                content = data['content'],
                post    = comment_post,
                user    = comment_user
            ).save()
        return JsonResponse({"message": "SUCCESS"}, status = 200)


# "id"          : 8,
# "name"        : "lightisblue",
# "email"       : "light@is.blue",
# "password"    : "$2b$12$DufrQgp6A3oDCNtGQAKcV.qYWK2lFpJkCSWW2WctIQkapVwOYizsG",
# "phone_number": "12452342",
# "created_at"  : "2020-08-11T21:44:05.492",
# "updated_at"  : "2020-08-11T21:44:05.492"

# url('posting/view_comment')
class CommentView(View):
    def get(self, request):
        # 1번 포스트의 커멘트들을 보여준다.
        comment = Comment.objects.filter(post=Post.objects.get(id=1)).values()
        # comment = Comment.objects.values()

        return JsonResponse({"message": list(comment)})