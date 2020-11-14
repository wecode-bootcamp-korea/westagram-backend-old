import json

from django.views import View
from django.http  import JsonResponse

from .models      import Post, Comment
from user.models  import User
from user.utils   import login_required


class CreatePostView(View):
    @login_required
    def post(self, request):
        data = json.loads(request.body)

        try:
            post_author  = request.user
            post_image   = data["image_url"]
            post_content = data["content"]

            Post.objects.create(
                author    = post_author,
                image_url = post_image,
                content   = post_content
            )
            return JsonResponse({"message":"SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status = 400)


class ReadPostView(View):
    @login_required
    def get(self, request):
        posts = Post.objects.all()

        if not posts:
            return JsonResponse({"message":"NO_POST"}, status = 404)

        result = [{
            "post_id"        : post.pk,
            "post_author"    : post.author.pk,
            "post_image_url" : post.image_url,
            "post_content"   : post.content,
            "posted_time"    : post.created_at
        } for post in posts]
        return JsonResponse({"results":result}, status = 200)


class CreateCommentView(View):
    @login_required
    def post(self, request):
        data = json.loads(request.body)

        try:
            post    = data["post_id"]
            content = data["comment_content"]

            if not Post.objects.filter(id = post).exists():
                return JsonResponse ({"message":"NO_POST"}, status = 400)

            if len(content) > 240:
                return JsonResponse ({"message":"TOO_LONG_CONTENT"}, status = 400)

            Comment.objects.create(
                post_id = post,
                author  = request.user,
                content = content
            )
            return JsonResponse ({"message":"SUCCESS"}, status =201)

        except KeyError:
            JsonResponse({"message":"KEY_ERROR"}, status = 400)


class ReadCommentView(View):
    @login_required
    def get(self, request):
        data = json.loads(request.body)

        try:
            post = data["post_id"]

            comments = Comment.objects.filter(post_id = post)
            print(comments)

            if not comments.exists():
                return JsonResponse({"message":"NO_COMMENT"}, status = 400)

            result = [{
                "author" : comment.author.pk,
                "content" : comment.content
            } for comment in comments]
            return JsonResponse ({"results":result} ,status = 201)

        except KeyError:
            JsonResponse({"message":"KEY_ERROR"}, status = 400)
