# autopep8: off
import json
import jwt
import datetime

from django.views           import View
from auth.models            import Users
from post.models            import *
from django.http            import JsonResponse
from django.db              import IntegrityError
from utils                  import signin_decorator
from django.core.exceptions import ObjectDoesNotExist


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

    @signin_decorator
    def put(self, request):
        data = json.loads(request.body)
        try:
            instance = Posts.objects.get(id=data.get('post_id'))
            writer_id = instance.user_id

            if writer_id != request.user.id:
                return JsonResponse({"message" : "NO_PERMISSION"}, status=403)
            else :
                instance.content = data.get('content')
                instance.save()
                return JsonResponse({"message" : "UPDATE_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({"message": "POST_DOES_NOT_EXIST"}, status=404)


    @signin_decorator
    def delete(self, request):
        data = json.loads(request.body)
        try:
            instance = Posts.objects.get(id=data.get('post_id'))
            writer_id = instance.user_id

            if writer_id != request.user.id:
                return JsonResponse({"message" : "NO_PERMISSION"}, status=403)
            else :
                instance.delete()
                return JsonResponse({"message" : "DELETE_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({"message": "POST_DOES_NOT_EXIST"}, status=404)

class Comment(View):
    @signin_decorator
    def post(self, request):
        data = json.loads(request.body)

        try:
            new_comment = Comments.objects.create(
                content    = data.get('content'),
                user       = request.user,
                post_id    = data.get('post_id'),
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

    @signin_decorator
    def put(self, request):
        data = json.loads(request.body)
        try:
            instance = Comments.objects.get(id=data.get('comment_id'))
            writer_id = instance.user_id

            if writer_id != request.user.id:
                return JsonResponse({"message" : "NO_PERMISSION"}, status=403)
            else :
                instance.content = data.get('content')
                instance.save()
                return JsonResponse({"message" : "UPDATE_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({"message": "COMMENT_DOES_NOT_EXIST"}, status=404)


    @signin_decorator
    def delete(self, request):
        data = json.loads(request.body)
        try:
            instance = Comments.objects.get(id=data.get('comment_id'))
            writer_id = instance.user_id

            if writer_id != request.user.id:
                return JsonResponse({"message" : "NO_PERMISSION"}, status=403)
            else :
                instance.delete()
                return JsonResponse({"message" : "DELETE_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({"message": "COMMENT_DOES_NOT_EXIST"}, status=404)

class ReComment(View):
    @signin_decorator
    def post(self, request):
        data = json.loads(request.body)

        try:
            new_comment = ReComments.objects.create(
                content    = data.get('content'),
                user       = request.user,
                comment_id    = data.get('comment_id'),
            )

            return JsonResponse({"message": "RE_COMMENT_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

    def get(self, request):
        comments = list(ReComments.objects
        .filter(comment_id = request.GET['comment_id'])
        .values('id',
                'content',
                'write_time',
                'update_time',
                'user_id',
                'comment_id',
                'user__name'))
        return JsonResponse(comments, safe=False)

    @signin_decorator
    def put(self, request):
        data = json.loads(request.body)
        try:
            instance = ReComments.objects.get(id=data.get('recomment_id'))
            writer_id = instance.user_id

            if writer_id != request.user.id:
                return JsonResponse({"message" : "NO_PERMISSION"}, status=403)
            else :
                instance.content = data.get('content')
                instance.save()
                return JsonResponse({"message" : "UPDATE_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({"message": "RE_COMMENT_DOES_NOT_EXIST"}, status=404)


    @signin_decorator
    def delete(self, request):
        data = json.loads(request.body)
        try:
            instance = ReComments.objects.get(id=data.get('recomment_id'))
            writer_id = instance.user_id

            if writer_id != request.user.id:
                return JsonResponse({"message" : "NO_PERMISSION"}, status=403)
            else :
                instance.delete()
                return JsonResponse({"message" : "DELETE_SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except IntegrityError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except ObjectDoesNotExist:
            return JsonResponse({"message": "RE_COMMENT_DOES_NOT_EXIST"}, status=404)

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
