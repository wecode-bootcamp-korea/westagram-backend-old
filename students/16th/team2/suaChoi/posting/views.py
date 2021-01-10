import json
import re

from django.http  import JsonResponse
from django.views import View

from westagram.settings import DATABASES
from .models            import Post, Comment, Like
from user.models        import User
from user.utils         import check_user

class PostView(View):

    @check_user
    def post(self, request):

        try:
            data      = json.loads(request.body)
            user      = request.user
            image_url = data['image_url']
            content   = data.get('content')

            Post.objects.create(user=user, image_url=image_url, content=content)
            return JsonResponse({"message": "SUCCESS"}, status=200)

        except:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    def get(self, request):
        posts     = Post.objects.all()
        post_list = []

        for post in posts:
            post_list.append({
                'user_id'    : post.user_id,
                'content'    : post.content,
                'image_url'  : post.image_url,
                'created_at' : post.created_at
            })
        return JsonResponse({"posts": post_list}, status=200)


class CommentView(View):

    @check_user
    def post(self, request, post_id):
        try:
            print(request.user)
            data    = json.loads(request.body)
            Comment.objects.create(
                post_id  = post_id,
                user_id  = request.user.id,
                comment  = data['comment']
            )
            return JsonResponse({"message": "SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except:
            return JsonResponse({"message": "ERROR"}, status=500)

    def get(self, request, post_id):
        post_id  = post_id
        post     = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post)

        comments_list = []
        for comment in comments:
            comments_list.append({
                'comment'    : comment.comment,
                'user_id'    : comment.user_id,
                'created_at' : comment.created_at
            })
        return JsonResponse({"comments": comments_list}, status=200)


class LikeView(View):

    @check_user
    def put(self, request, post_id):

        try:
            user = request.user.id
            post = Post.objects.get(id=post_id).id
            like = Like.objects.filter(user_id=user, post_id=post)

            if like.first() is not None:
                if like.first().is_deleted == False:
                    like.update(is_deleted=True)
                    return JsonResponse({"message": "CANCEL_LIKE"}, status=200)
                else:
                    like.update(is_deleted=False)
                    return JsonResponse({"message": "SUCCESS"}, status=200)

            elif like.first() is None:
                Like.objects.create(
                    user_id = user,
                    post_id = post
                )

            return JsonResponse({"message": "SUCCESS"}, status=200)

        except Exception as e:
            return JsonResponse({"error":(e.args[0])}, status=500)
