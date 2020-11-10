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

        NECESSERY_KEYS = ('user_id', 'content', 'image_url')
        data = json.loads(request.body)

        if list(filter(lambda x: x not in data.keys(),NECESSERY_KEYS)):
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        try:
            post    = Post.objects.create(content = data['content'],
                                          image   = data['image_url'],
                                          user_id = data['user_id'],
                                          )
            post.save()
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except IntegrityError:
            return JsonResponse({'message': 'NOT_EXIST_USER'}, status=400)

    @login_decorator
    def get(self, request):
        return JsonResponse({'data' : list(Post.objects.values())}, status=200)

class CommentView(View):

    @login_decorator
    def post(self, request):
        NECESSERY_KEYS = ('user_id', 'post_id', 'content')
        data = json.loads(request.body)

        for k in NECESSERY_KEYS:
            if k not in data.keys():
                return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

        if User.objects.filter(id=data['user_id']).exists() and \
           Post.objects.filter(id=data['post_id']).exists():

           Comment.objects.create(
                user    = data['user_id'],
                post    = data['post_id'],
                content = data['content'],
           )
           return JsonResponse({'message': 'SUCCESS'}, status=201)

        return JsonResponse({'message': 'NOT_EXIST_USER'}, status=400)
