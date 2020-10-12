# autopep8: off
import json
import jwt
import datetime

from django.views import View
from auth.models  import Users
from post.models  import *
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

class Comment(View):
    @signin_decorator
    def post(self, request):
        data = json.loads(request.body)

        try:
            new_comment = Comments.objects.create(
                content    = data.get('content'),
                user       = request.user,
                post_id    = data.get('post_id'),
                comment_id = data.get('comment_id')
            )

            return JsonResponse({"message": "COMMENT_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    def get(self, request):
        comments = list(Comments.objects
        .filter(post_id = request.GET['post_id'])
        .values('id',
                'content',
                'write_time',
                'update_time',
                'user_id',
                'post_id',
                'comment_id',
                'user__name'))
        return JsonResponse(comments, safe=False)

class Like(View):
    @signin_decorator
    def post(self, request):
        data = json.loads(request.body)

        try:
            PostLikes.objects.create(
                user       = request.user,
                post_id    = data.get('post_id'),
            )

            return JsonResponse({"message": "LIKE_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
