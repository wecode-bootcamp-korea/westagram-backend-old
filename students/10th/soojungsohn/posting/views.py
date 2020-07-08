import json

from django.views   import View
from django.http    import JsonResponse

from .models     import (
    Post,
    Comment
)
from user.models import User

class PostingView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(id=data['user_id']).exists():
                user = User.objects.get(id=data['user_id'])
                Post(
                    user = user,
                    text = data['text']
                ).save()
                return JsonResponse({'message' : 'SUCCESS'}, status=200)
            return JsonResponse({'message' : 'UNAUTHORIZED'}, status = 401)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if (User.objects.filter(id=data['user_id']).exists()) and (Post.objects.filter(id=data['post_id']).exists()):
                user = User.objects.get(id = data['user_id'])
                post = Post.objects.get(id = data['post_id'])
                Comment(
                    user = user,
                    post = post,
                    text = data['text']
                ).save()
                return JsonResponser({'message' : 'SUCCESS'}, status=200)
            return JsonResponse({'message' : 'UNAUTHORIZED'}, status=401)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=200)
