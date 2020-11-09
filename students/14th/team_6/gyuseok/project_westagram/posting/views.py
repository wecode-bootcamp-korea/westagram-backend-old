import json
from django.views import View
from django.http  import JsonResponse
from .models import Post, Comment
from user.models import User
from django.db.models import Q

from django.template import loader

class CreateBoardView(View):
    def post(self, request):

        NECESSERY_KEYS = ('username', 'content', 'image_url')
        data = json.loads(request.body)

        for k in NECESSERY_KEYS:
            if k not in data.keys():
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)


        if User.objects.filter(name=data['username']).exists():
            key = User.objects.get(name=data['username'])
            Post.objects.create( content = data['content'],
                                 image   = data['image_url'],
                                 user    = key
                               )
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        else:
            return JsonResponse({'message': 'NOT EXIST USER'}, status=400)


class ReadBoardView(View):
    def get(self, request):
        return JsonResponse({'data' : list(Post.objects.values())}, status=200)

class CreateCommentView(View):
    def post(self, request):
        NECESSERY_KEYS = ('user_id', 'post_id', 'content')
        data = json.loads(request.body)

        for k in NECESSERY_KEYS:
            if k not in data.keys():
                return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        if User.objects.filter(id=data['user_id']).exists() and \
           Post.objects.filter(id=data['post_id']).exists():

           Comment.objects.create(
                user    = User.objects.get(id=data['user_id']),
                post    = Post.objects.get(id=data['post_id']),
                content = data['content'],
           )
           return JsonResponse({'message': 'SUCCESS'}, status=201)
        else:
           return JsonResponse({'message': 'NOT EXIST USER'}, status=400)
