import json

from django.views import View
from django.http  import JsonResponse

from .models      import Post
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
            return JsonResponse({"message" : "SUCCESS"}, status = 201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)

class ReadPostView(View):
    @login_required
    def get(self,request):
        data    = json.loads(request.body)
        post_id = data["post_id"]

        try:
            post_query = Post.objects.filter(pk = post_id)
            result  = []

            if post_query.exists():
                post = post_query.first()

                post_dict = {
                    "post_id"        : post.pk,
                    "post_author"    : post.author_id,
                    "post_image_url" : post.image_url,
                    "post_content"   : post.content,
                    "posted_time"    : post.created_at
                }
                result.append(post_dict)
                return JsonResponse({"result" : result}, status = 200)
            return JsonResponse({"message" : "NO_POST"}, status = 400)

        except KeyError:
            JsonResponse({"message" : "KEY_ERROR"}, status = 400)
#        except JSONDecodeError:
#            JsonResponse({"message" : "VALUE_ERROR"}, status = 400)
