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

    @signin_decorator
    def get(self, request):
        user_id = request.user.id
        follow_list = []

        follows = Follows.objects.filter(followed_by=user_id)

        for follow in follows:
            follow_list.append(follow.user_id)

        print(follow_list)
        posts = []
        for post in Posts.objects.filter(user_id__in=follow_list):
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
            user    = request.user
            post_id = data.get('post_id')
            if not PostLikes.objects.filter(user = user, post_id = post_id).exists() :
                PostLikes.objects.create(
                    user       = user,
                    post_id    = post_id,
                )
                return JsonResponse({"message": "LIKE_SUCCESS"}, status=200)
            else :
                return JsonResponse({"message": "ALLREADY_LIKED"}, status=400) 



        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class Follow(View):
    @signin_decorator
    def post(self, request):
        data = json.loads(request.body)

        try:
            user_id     = data.get('user_id')
            followed_by = request.user
            if not Follows.objects.filter(user_id=user_id, followed_by=followed_by).exists():
                Follows.objects.create(
                    user_id     = user_id,
                    followed_by = followed_by,
                )
                return JsonResponse({"message": "FOLLOW_SUCCESS"}, status=200)

            else :
                return JsonResponse({"message": "ALLREADY_FOLLOWING"}, status=400) 

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)
