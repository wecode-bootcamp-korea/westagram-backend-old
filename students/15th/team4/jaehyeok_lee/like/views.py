import json

from django.http import JsonResponse
from django.views import View

from post.models import Post
from user.models import User
from like.models import Like
from user.utils  import id_auth

# Create your views here.

class LikeView(View):
    @id_auth
    def post(self, request):
        data = json.loads(request.body)

        try:
            data_like_user  = request.user
            data_liked_post = Post.objects.get(id = data['post_id'])
            
            if Like.objects.filter(like_user_id = data_like_user, liked_post_id = data_liked_post):
                Like.objects.get(like_user_id = data_like_user, liked_post_id = data_liked_post).delete()
                return JsonResponse({"message": "SUCCESS_UNLIKE"}, status = 200)
            else:
                Like.objects.create(like_user = data_like_user, liked_post = data_liked_post)
                return JsonResponse({"message": "SUCCESS_LIKE"}, status = 200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status = 400)
        except AssertionError:
            return JsonResponse({"message": "ALREADY_LIKED"}, status = 400)

