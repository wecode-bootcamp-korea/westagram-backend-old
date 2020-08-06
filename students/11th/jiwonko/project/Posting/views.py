import json

from django.views import View
from django.http  import JsonResponse
from django.core  import serializers

from .models     import Post, Comment
from User.models import User

class PostView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(id = data['user_id']).exists():
                user = User.objects.get(id = data['user_id'])
                Post(
                    user    = user,
                    content = data['content'],
                    img_url = data['img_url']
                ).save()
                return JsonResponse({'message' : 'SUCCESS'}, status = 200)
            return JsonResponse({'message' : 'NO_EXISTS_USER'}, status = 401)
        except KeyError:
                return JsonResponse({'message' : 'KEY_ERROR'}, status = 401)

class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            user = User.objects.get(id = data['user_id'])
            post = Post.objects.get(id = data['post_id'])
            Comment(
            user    = user,
            post    = post,
            comment = data['comment']
            ).save()
            return JsonResponse({'message' : 'SUCCESS'}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_USER'}, status = 400)

class ListCommentView(View):
    def get(self, request):
        comments = Comment.objects.filter(post = 1)
        return JsonResponse(serializers.serialize('json', comments), safe = False, status = 200)