# autopep8: off
import json
import jwt
import datetime

from django.views import View
from auth.models  import Users
from post.models  import Posts, PostImage
from django.http  import JsonResponse
from django.db    import IntegrityError
from utils        import signin_decorator


class Post(View):
    @signin_decorator
    def post(self, request):
        data = json.loads(request.body)

        try:
            new_post = Posts.objects.create(
                content = data.get('content'),
                user    = request.user
            )
            if data.get('urls'):
                for url in data.get('urls'):
                    PostImage.objects.create(
                        url  = url,
                        post = new_post
                    )

            return JsonResponse({"message": "POST_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    def get(self, request):
        posts = []
        for post in Posts.objects.all():
            posts.append(post.get_json())
        return JsonResponse(posts, safe=False)
