import json

from django.views import View
from django.http  import JsonResponse
from django.core  import serializers

from User.models import User
from User.utils  import validate_token
from .models     import Post, Comment

class PostView(View):
    @validate_token
    def post(self, request):
        data = json.loads(request.body)

        if 'user' in data and 'img_url' in data and 'content' in data:
            user    = data['user']
            img_url = data['img_url']
            content = data['content']
        else:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        if not User.objects.filter(email = user):
            return JsonResponse({'message':'You did not join'}, status = 400)

        user = User.objects.get(email = user)

        Post(
            user    = user,
            img_url = img_url,
            content = content
        ).save()

        return JsonResponse({'message':'SUCCESS'}, status = 200)

class GetView(View):
    def get(self, request):
        post = Post.objects.all()

        return JsonResponse(serializers.serialize('json', post),safe = False, status = 200)

class CommentPost(View):
    def post(self, request):
        data = json.loads(request.body)

        if 'user' in data and 'post' in data and 'comment' in data:
            user    = data['user']
            post    = data['post']
            comment = data['comment']
        else:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        if not User.objects.filter(email = user):
            return JsonResponse({'message':'You did not join'}, status = 400)

        user = User.objects.get(email = user)

        if not Post.objects.filter(id = post):
            return JsonResponse({'message':'Post is not existed'}, status = 400)

        post = Post.objects.get(id = post)

        Comment(
            user    = user,
            post    = post,
            comment = comment
        ).save()

        return JsonResponse({'message':'SUCCESS'}, status = 200)

class CommentGet(View):
    def get(self, request):
        comment = Comment.objects.filter(post = 1)

        return JsonResponse(serializers.serialize('json', comment), safe = False, status = 200)
