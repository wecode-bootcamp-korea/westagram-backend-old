import json

from django.views import View
from django.http import JsonResponse, HttpResponse

from .models import (
    Post,
    Comment
)
from user.models import User

class PostingView(View):
    def post(self, request):
        data = json.loads(request.body)
        if User.objects.filter(id=data['user_id']).exists():
            user = User.objects.get(id=data['user_id'])
            Post(
                user = user,
                text = data['text']
                ).save()
        else:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        return JsonResponse({'message' : 'POSTING SUCCESS'}, status=200)

class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)
        if (User.objects.filter(id=data['user_id']).exists()) and (Post.objects.filter(id=data['post_id']).exists()):
            user = User.objects.get(id = data['user_id'])
            post = Post.objects.get(id = data['post_id'])
            Comment(
                user = user,
                post = post,
                text = data['text']
                    ).save()
        else:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        return JsonResponse({'message' : 'ADD COMMENT SUCCESS'}, status=200)
