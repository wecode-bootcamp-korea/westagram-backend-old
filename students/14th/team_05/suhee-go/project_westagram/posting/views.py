import json

from django.views import View
from django.http  import JsonResponse

from .models      import Post
from user.models  import User

class CreatePostView(View):
    @login_required
    def post(self,request):
        data = json.loads(request.body)

        post_author  = data["user_id"]
        post_image   = data["image_url"]
        post_content = data["content"]

        try:
            if not User.objects.filter(pk = post_author).exists():
                return JsonResponse({"message" : "USER_NOT_EXIST"}, status = 400)

            Post.objects.create(
                author_id = post_author,
                image     = post_image,
                content   = post_content
            )
            return JsonResponse({"message" : "SUCCESS"}, status = 201)

        except KeyError:
            JsonResponse({"message" : "KEY_ERROR"}, status = 400)

class ReadPostView(View):
    @login_required
    def get(self,request):
        data    = json.loads(request.body)
        post_id = data["post_id"]

        try:
            post_query = Post.objects.filter(pk = post_id)
            result  = []

            if post_query.exists():
                for post in post_query:
                    post_dict = {
                        "post_id"        : post.pk,
                        "post_author"    : post.author_id,
                        "post_image_url" : post.image_url,
                        "post_content"   : post.content,
                        "post_time"      : post.created_at
                    }
                    result.append(post_dict)
                    return JsonResponse({"result" : result}, status = 200)
                return JsonResponse({"message" : "NO_POST"}, status = 400)

        except KeyError:
            JsonResponse({"message" : "KEY_ERROR"}, status = 400)

