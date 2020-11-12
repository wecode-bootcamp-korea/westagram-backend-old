import json

from django.views import View
from django.http  import JsonResponse
from django.db.models import Q
from django.db import IntegrityError

from .models     import Post, Comment
from user.models import User
from user.utils  import login_decorator
class BoardView(View):
    @login_decorator
    def post(self, request):
        NECESSERY_KEYS = ('content', 'image_url')
        data = json.loads(request.body)

        if list(filter(lambda x: x not in data.keys(),NECESSERY_KEYS)):
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        Post.objects.create(content   = data['content'],
                            image_url = data['image_url'],
                            user_id   = request.user_id,
                            )
        return JsonResponse({'message': 'SUCCESS'}, status=201)

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

        for k in NECESSERY_KEYS:
            if k not in data.keys():
                return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        if User.objects.filter(id=data['post_id']).exists():

           Comment.objects.create(
                user    = request.user_id,
                post    = data['post_id'],
                content = data['content'],
           )
           return JsonResponse({'message': 'SUCCESS'}, status=201)

        return JsonResponse({'message': 'NOT_EXIST_POST'}, status=400)
