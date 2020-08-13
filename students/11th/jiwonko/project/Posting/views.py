import json

from django.views import View
from django.http  import JsonResponse
from django.core  import serializers

from .models     import Post, Comment
from User.models import User
from User.utils  import login_required

class PostView(View):
    @login_required
    def post(self, request):
        data = json.loads(request.body)
        try:
            if User.objects.filter(email = data['user']).exists():
                user = User.objects.get(email = data['user'])
                Post(
                    user    = request.user.email,
                    content = data['content'],
                    img_url = data['img_url'],
                ).save()
                return JsonResponse({'message' : 'SUCCESS'}, status = 200)
            return JsonResponse({'message' : 'NO_EXISTS_USER'}, status = 401)
        except KeyError:
                return JsonResponse({'message' : 'KEY_ERROR'}, status = 401)

    def get(self, request):
        post_data = Post.objects.values()
        return JsonResponse({'post_data' : list(post_data)}, status = 200)

class CommentView(View):
    @login_required
    def post(self, request):
        data = json.loads(request.body)
        try:
            Comment(
            user    = request.user.email,
            post_id = data['post'],
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