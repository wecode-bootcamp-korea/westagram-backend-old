import json

from django.views import View
from django.http import JsonResponse

from User.models import User
from .models import Post, Comment

class PostingView(View):
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(name = data['name'])
        Post(
            name    = user,
            image   = data['image'],
            content = data['content']
        ).save()

    def get(self, request):
        posting_data = Post.objects.values()
        return JsonResponse(
            {"positng_data":list(posting_data)},
            status = 200
        )

class CommentView(View):
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(name = data['name'])
        post = Post.objects.get(content = data['content'])
        Comment(
            name    = user,
            post    = post,
            comment = data['comment']
        ).save()

    def get(self, request):
        first_posting = Comment.objects.filter(post_id = 1)
        comment_data = first_posting.values()
        return JsonResponse(
            {"comment_data":list(comment_data)},
            status = 200
        )
