import json

from django.views import View
from django.http import JsonResponse

from .models import (
    Post,
    Comment
)
from user.models import User

class PostingView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user_id = data['user_id']
            text    = data['text']
            
            if User.objects.filter(id=user_id).exists():
                user = User.objects.get(id=user_id)
                Post(
                    user = user,
                    text = text
                ).save()
                return JsonResponse({'message' : 'POSTING SUCCESS'}, status=200)
            else:
                return JsonResponse({'message' : 'NO EXISTING USER'}, status = 401)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user_id = data['user_id']
            post_id = data['post_id']
            text    = data['text']
            
            if (User.objects.filter(id=user_id).exists()) and (Post.objects.filter(id=post_id).exists()):
                user = User.objects.get(id = user_id)
                post = Post.objects.get(id = post_id)
                Comment(
                    user = user,
                    post = post,
                    text = text
                    ).save()
                return JsonResponser({'message' : 'ADD COMMENT SUCCESS'}, status=200)
            else:
                return JsonResponse({'message' : 'NO EXISTING USER OR POST'}, status=401)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=200)
