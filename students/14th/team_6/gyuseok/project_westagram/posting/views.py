import json

from django.views import View
from django.http  import JsonResponse
from django.db.models import Q
from django.db import IntegrityError

from .models     import Post, Comment, Like
from user.models import User
from user.utils  import login_decorator

class BoardView(View):
    @login_decorator
    def post(self, request):
        NECESSERY_KEYS = ('content', 'image_url')
        data = json.loads(request.body)

        if list(filter(lambda x: x not in data,NECESSERY_KEYS)):
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        Post.objects.create(content   = data['content'],
                            image_url = data['image_url'],
                            user_id   = request.user_id,
                            )
        return JsonResponse({'message' : 'SUCCESS'}, status=201)

    @login_decorator
    def get(self, request):
        return JsonResponse({'data' : list(Post.objects.values())}, status=200)

    @login_decorator
    def delete(self, request):
        pass

class CommentView(View):

    @login_decorator
    def post(self, request):
        NECESSERY_KEYS = ('post_id', 'content')
        data = json.loads(request.body)

        if list(filter(lambda x: x not in data,NECESSERY_KEYS)):
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        if User.objects.filter(id=data['post_id']).exists():

           Comment.objects.create(
                user_id = request.user_id,
                post_id = data['post_id'],
                content = data['content'],
           )
           return JsonResponse({'message' : 'SUCCESS'}, status=201)

        return JsonResponse({'message' : 'NOT_EXIST_POST'}, status=400)

class LikeView(View):

    @login_decorator
    def post(self, request):
        NECESSERY_KEYS = ('post_id',)
        data = json.loads(request.body)

        if list(filter(lambda x: x not in data,NECESSERY_KEYS)):
            return JsonResponse({'message' : f'KEY_ERROR'}, status=400)

        if User.objects.filter(id=data['post_id']).exists():
            if not Like.objects.filter(post_id=data['post_id']).exists():
                Like.objects.create(
                    user_id = request.user_id,
                    post_id = data['post_id'],
                )
                return JsonResponse({'message' : 'SUCCESS'}, status=201)
            else:
                Like.objects.filter(
                    post_id=data['post_id'],
                    user_id=request.user_id
                ).delete()

                return JsonResponse({'message' : 'SUCCESS_DELETE'}, status=200)

        return JsonResponse({'message' : 'NOT_EXIST_POST'}, status=400)

    def get(self, request):
        NECESSERY_KEYS = ('post_id',)
        data = json.loads(request.body)

        if list(filter(lambda x: x not in data,NECESSERY_KEYS)):
            return JsonResponse({'message' : f'KEY_ERROR'}, status=400)

        if User.objects.filter(id=data['post_id']).exists():

           the_post_like = Like.objects.filter(post_id = data['post_id']).count()

           context = {
               'message' : 'SUCCESS',
               'data' : {
                   'like' : the_post_like
               }
           }
           return JsonResponse(context, status=200)

        return JsonResponse({'message' : 'NOT_EXIST_POST'}, status=400)

